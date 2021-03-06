import React, { PureComponent } from 'react'
import axios from 'axios'
import queryString from 'query-string'
import moment, { isMoment } from 'moment'

import {
	DATE_FORMAT,
	GENERAL_ID,
} from '~/filtering/constants'
import FilterAccordion from '~/filtering/FilterAccordion'
import FiltersCategorySelection from '~/filtering/FiltersCategorySelection'
import FiltersHeader from '~/filtering/FiltersHeader'
import FiltersExpandable from '~/filtering/FiltersExpandable'
import FiltersFooter from '~/filtering/FiltersFooter'


class IncidentFiltering extends PureComponent {
	constructor(props, ...args) {
		super(props, ...args)

		this.handleToggle = this.handleToggle.bind(this)
		this.handleSelection = this.handleSelection.bind(this)
		this.handleApplyFilters = this.handleApplyFilters.bind(this)
		this.handleClearFilters = this.handleClearFilters.bind(this)
		this.handleFilterChange = this.handleFilterChange.bind(this)
		this.handlePopState = this.handlePopState.bind(this)

		this.state = {
			filtersExpanded: false,
			loading: 0,
			filtersTouched: false,
			...this.getStateFromQueryParams(),
		}
		if (props.category) {
			this.state.categoriesEnabled[props.category] = true
		}
	}

	componentDidMount() {
		window.addEventListener('popstate', this.handlePopState)
	}

	componentWillUnmount() {
		window.removeEventListener('popstate', this.handlePopState)
	}

	getStateFromQueryParams() {
		// Initializes the state on page load. Returns three variables:
		// - categoriesEnabled: object that contains `true` values
		//   for selected category ids
		// - filterValues: object mapping filter names to filter value
		// - startExpanded: object that contains `true` values for ids of
		//   categories that should be expanded when the page loads. This will
		//   be the general category plus either the category for the current page
		//   or categories that contain filter values.
		const params = queryString.parse(location.search)

		const categoriesEnabled = {
			[GENERAL_ID]: true,
		}
		if (params.categories) {
			params.categories.split(',').forEach(
				id => { categoriesEnabled[id] = true }
			)
		}

		// Include filterValues for non-enabled categories as well,
		// so that filter summary can show they're enabled.
		const filterValues = this.props.categories.reduce((acc, category) => {
			const newAcc = { ...acc }

			category.filters.forEach(filter => {
				if (filter.type === 'date') {
					const lowerDate = `${filter.name}_lower`
					const upperDate = `${filter.name}_upper`
					if (params[lowerDate]) newAcc[lowerDate] = moment(params[lowerDate]).toDate()
					if (params[upperDate]) newAcc[upperDate] = moment(params[upperDate]).toDate()
				} else if (filter.type === 'autocomplete' && params[filter.name]) {
					if (filter.many) {
						newAcc[filter.name] = params[filter.name]
							.split(',')
							.map(id => ({ id: parseInt(id) }))
					} else {
						newAcc[filter.name] = { id: parseInt(params[filter.name]) }
					}
				} else if (params[filter.name]) {
					newAcc[filter.name] = params[filter.name]
				}
			})

			return newAcc
		}, {})

		if (this.props.noCategoryFiltering && this.props.category) {
			filterValues.categories = [this.props.category]
		}

		// Expand initially if it's the general category, if it's the
		// category page, or if at least one filter has a value.
		const startExpanded = {
			[GENERAL_ID]: true,
		}

		if (this.props.noCategoryFiltering && this.props.category) {
			startExpanded[this.props.category] = true
		} else {
			this.props.categories.forEach(category => {
				if (category.id === GENERAL_ID) return

				startExpanded[category.id] = category.filters.some(filter => {
					if (filter.type === 'date') {
						return filterValues[`${filter.name}_lower`] || filterValues[`${filter.name}`]
					}
					return filterValues[filter.name]
				})
			})
		}

		return {
			categoriesEnabled,
			filterValues,
			startExpanded,
		}
	}

	getPageFetchParams() {
		const {
			categories,
		} = this.props
		const {
			categoriesEnabled,
			category,
			filterValues,
			noCategoryFiltering,
		} = this.state

		let categoriesParam
		if (noCategoryFiltering && category) {
			categoriesParam = null
		} else {
			categoriesParam = Object.keys(categoriesEnabled).filter(
				// Convert GENERAL_ID to string because object keys are
				// always strings.
				id => id !== `${GENERAL_ID}` && categoriesEnabled[id]
			).join(',')
		}

		const params = {}

		categories.forEach(cat => {
			if (!categoriesEnabled[cat.id]) return

			cat.filters.forEach(filter => {
				if (filter.type === 'date') {
					const lowerDate = `${filter.name}_lower`
					const upperDate = `${filter.name}_upper`
					if (filterValues[lowerDate]) {
						params[lowerDate] = moment(filterValues[lowerDate]).format(DATE_FORMAT)
					}
					if (filterValues[upperDate]) {
						params[upperDate] = moment(filterValues[upperDate]).format(DATE_FORMAT)
					}

					// If date filter values were entered backwards, swap them.
					const hasCompleteRange = (
						params[lowerDate] &&
						params[upperDate] &&
						params[upperDate] !== params[lowerDate]
					)
					const shouldSwap = (
						hasCompleteRange &&
						params[lowerDate] > params[upperDate]
					)
					if (shouldSwap) {
						[params[lowerDate], params[upperDate]] = [params[upperDate], params[lowerDate]]
					}

					return
				}

				const value = filterValues[filter.name]
				if (!value) return

				if (filter.type === 'autocomplete') {
					if (Array.isArray(value)) {
						params[filter.name] = value.map(({ id }) => id).join(',')
					} else {
						params[filter.name] = value.id
					}
				} else {
					params[filter.name] = value
				}
			})
		})

		if (categoriesParam) {
			params.categories = categoriesParam
		} else if (params.hasOwnProperty('categories')) {
			delete params.categories
		}

		return params
	}

	/**
	 * We want to redirect to a CategoryPage or IncidentIndexPage when the Apply
	 * Filters button is hit on a page that isn't of those types. This function
	 * determines which page should be redirected to based on the number of
	 * categories. If only one category is whitelisted, just redirect to that
	 * CategoryPage.
	 */
	getExternalUrl() {
		const { categoriesEnabled } = this.state
		const selectedCategories = this.props.categories.filter(
			({ id }) => categoriesEnabled[id] && id !== GENERAL_ID
		)

		if (selectedCategories.length === 1) {
			return selectedCategories[0].url
		}

		return this.props.external
	}

	handleToggle() {
		this.setState({
			filtersExpanded: !this.state.filtersExpanded,
		})
	}

	handleSelection(id) {
		this.setState(previousState => {
			return {
				...previousState,
				categoriesEnabled: {
					...previousState.categoriesEnabled,
					[id]: !previousState.categoriesEnabled[id],
				},
				startExpanded: {
					...previousState.startExpanded,
					[id]: !previousState.startExpanded[id],
				},
				filtersTouched: true,
			}
		})
	}

	handlePopState() {
		this.setState(
			this.getStateFromQueryParams(),
			() => this.fetchPage(this.getPageFetchParams())
		)
	}

	handleApplyFilters(e) {
		e.preventDefault()

		const params = this.getPageFetchParams()

		const qs = '?' + queryString.stringify(params)
		if (this.props.applyExternally) {
			window.location = this.getExternalUrl() + qs
		} else {
			history.pushState(null, null, qs)
			this.fetchPage(params)
		}

		// Once filters are set in page params, make sure the
		// state reflects that. These could get out of sync, for example,
		// if a filter for a non-selected category has a value in state
		// (because that value would not get sent to the server.)
		this.setState(this.getStateFromQueryParams())
	}

	handleClearFilters() {
		this.setState({
			filterValues: {},
			filtersTouched: false,
			categoriesEnabled: { [GENERAL_ID]: true },
		})
		if (this.props.category) {
			this.setState({
				categoriesEnabled: { [this.props.category]: true }
			})
		}

		history.pushState(null, null, '?')
		this.fetchPage({})
	}

	fetchPage(params) {
		this.setState({
			loading: this.state.loading + 1,
			filtersTouched: false,
		})

		axios.get('?' + queryString.stringify(params))
			.then(
				response => {
					this.setState({
						loading: this.state.loading - 1,
					})

					if (response.status === 200) {
						if (!window._incidentLoader) {
							console.warn('No IncidentLoader instance found.')
							return
						}
						window._incidentLoader.replaceIncidents(
							response.data,
						)
					}
				},

				() => {
					this.setState({
						loading: this.state.loading - 1,
					})
				}
			)
	}

	handleFilterChange(label, event) {
		let value
		if (!event) {
			value = null
		} else if (isMoment(event) || event instanceof Date) {
			value = event
		} else if (event.target && event.target.hasOwnProperty('checked')) {
			value = event.target.checked
		} else if (event.target) {
			value = event.target.value
		}

		this.setState({
			filterValues: {
				...this.state.filterValues,
				[label]: value,
			},
			filtersTouched: true,
		})
	}

	render() {
		const {
			categoriesEnabled,
			filterValues,
			filtersExpanded,
			filtersTouched,
			startExpanded,
		} = this.state

		const {
			categories,
			noCategoryFiltering,
			changeFiltersMessage,
			exportPath,
		} = this.props

		return (
			<div className="filters">
				<form onSubmit={this.handleApplyFilters}>
					<FiltersHeader
						categories={categories}
						categoriesEnabled={categoriesEnabled}
						changeFiltersMessage={changeFiltersMessage}
						filterValues={filterValues}
						filtersExpanded={filtersExpanded}
						handleToggle={this.handleToggle}
					/>

					<FiltersExpandable filtersExpanded={filtersExpanded}>
						{!noCategoryFiltering && (
							<FiltersCategorySelection
								categories={categories.filter(({ id }) => id !== GENERAL_ID)}
								categoriesEnabled={categoriesEnabled}
								handleSelection={this.handleSelection}
							/>
						)}

						<ul className="filters__body">
							{categories.map(category => {
								if (!categoriesEnabled[category.id]) return null

								return (
									<FilterAccordion
										key={category.id}
										category={category}
										collapsible={noCategoryFiltering ? false : category.id !== GENERAL_ID}
										handleFilterChange={this.handleFilterChange}
										filterValues={filterValues}
										startExpanded={startExpanded[category.id]}
									/>
								)
							})}
						</ul>

						<FiltersFooter
							handleClearFilters={this.handleClearFilters}
							pageFetchParams={this.getPageFetchParams()}
							loading={this.state.loading}
							filtersTouched={filtersTouched}
							exportPath={exportPath}
						/>
					</FiltersExpandable>
				</form>
			</div>
		)
	}
}


export default IncidentFiltering
