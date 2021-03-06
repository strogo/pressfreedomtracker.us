import React, { PureComponent } from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'

import Single from './Single'
import Multi from './Multi'


class Autocomplete extends PureComponent {
	constructor(props, ...args) {
		super(props, ...args)

		this.handleClick = this.handleClick.bind(this)
		this.handleChange = this.handleChange.bind(this)
		this.handleCreate = this.handleCreate.bind(this)

		this.state = {
			value: props.value,
			input: {
				value: '',
			},
			suggestions: [],
		}

		if (props.fetchInitialValues) {
			this.fetchInitialValues(props.value)
		}
	}

	componentDidMount() {
		this.checkNewSuggestions('', false)
	}

	get value() {
		if (this.props.controlled) {
			if ((Array.isArray(this.props.value) && !!this.props.value[0] && !this.props.value[0].title)
				|| (!!this.props.value && this.props.value.constructor === Object && !this.props.value.title)) {
				this.fetchInitialValues(this.props.value)
			}
			return this.props.value
		} else {
			return this.state.value
		}
	}

	handleChange(event) {
		const { value } = event.target
		this.checkNewSuggestions(value)
		this.setState({
			input: {
				...this.state.input,
				value,
			}
		})
	}

	getExclusions() {
		const { value } = this.state
		if (!value) {
			return ''
		}

		if (this.props.isSingle && value) {
			return value.id
		}

		return value.map(({ id }) => id).join(',')
	}

	checkNewSuggestions(value, checkDifferent = true) {
		if (checkDifferent && value === this.state.value) {
			return
		}

		const params = {
			query: value,
			type: this.props.type,
			exclude: this.getExclusions(),
		}
		axios.get(this.props.apiBase + 'search/', { params })
			.then(res => {
				if (res.status !== 200) {
					return
				}

				if (!Array.isArray(res.data.items)) {
					return
				}
				res.data.items.map(item => item.id = item.pk)

				this.setState({
					suggestions: res.data.items
				})
			})
	}

	fetchInitialValues(value) {
		if (!value) {
			return
		}

		const isMulti = Array.isArray(value)
		if (isMulti && value.length === 0) {
			return
		}

		if (isMulti) {
			var pks = value.map(({ id }) => id).join(',')
		} else {
			var pks = value.id
		}

		const params = {
			pks,
			type: this.props.type,
		}
		axios.get(this.props.apiBase + 'objects/', { params })
			.then(res => {
				if (res.status !== 200) {
					return
				}

				if (!Array.isArray(res.data.items)) {
					return
				}
				res.data.items.map(item => item.id = item.pk)

				let newValue
				if (isMulti) {
					newValue = this.state.value.map(v => {
						// "Pages" is actually items, not paginated groups. This is probably a
						// remnant of this being built specifically for wagtail pages.
						const page = res.data.items.find(page => page.id === v.id)
						if (!page) {
							return v
						}

						return page
					})
				} else {
					newValue = res.data.items[0]
				}

				this.setState({ value: newValue })

				if (typeof this.props.onChange === 'function') {
					this.props.onChange({ target: { value: newValue } })
				}
			})
	}

	handleClick(value) {
		this.setState({ value })

		if (typeof this.props.onChange === 'function') {
			this.props.onChange({ target: { value, _autocomplete: true } })
		}
	}

	handleCreate() {
		const { value } = this.state.input
		if (value.trim() === '') {
			return
		}

		const data = new FormData()
		data.set('type', this.props.type)
		data.set('value', value)
		axios.post(this.props.apiBase + 'create/', data)
			.then(res => {
				if (res.status !== 200) {
					this.setState({ isLoading: false })
					return
				}

				const value = this.props.isSingle ? res.data : (this.state.value || []).concat(res.data)

				this.setState({
					isLoading: false,
					value,
				})

				if (typeof this.props.onChange === 'function') {
					this.props.onChange({ target: { value } })
				}
			})
		this.setState({ isLoading: true })
	}

	render() {
		const { name, isSingle, onChange } = this.props
		const { input, suggestions } = this.state

		const canCreate = this.props.canCreate && input.value.trim() !== ''
		const useHiddenInput = typeof onChange !== 'function'

		return (
			<span className="autocomplete">
				{useHiddenInput && (
					<input
						type="hidden"
						value={JSON.stringify(this.value)}
						name={name}
					/>
				)}

				{isSingle && (
					<Single
						input={input}
						suggestions={suggestions}
						selected={this.value}

						canCreate={canCreate}

						onCreate={this.handleCreate}
						onChange={this.handleChange}
						onClick={this.handleClick}
					/>
				)}

				{!isSingle && (
					<Multi
						input={input}
						suggestions={suggestions}
						selections={this.value || Multi.defaultProps.selections}

						canCreate={canCreate}

						onCreate={this.handleCreate}
						onChange={this.handleChange}
						onClick={this.handleClick}
					/>
				)}
			</span>
		)
	}
}


Autocomplete.defaultProps = {
	fetchInitialValues: false,
	controlled: false,
}


Autocomplete.propTypes = {
	name: PropTypes.string.isRequired,
	type: PropTypes.string.isRequired,
	canCreate: PropTypes.bool.isRequired,
	isSingle: PropTypes.bool.isRequired,
	onChange: PropTypes.func,
	fetchInitialValues: PropTypes.bool,
	apiBase: PropTypes.string.isRequired,
	controlled: PropTypes.bool.isRequired,
}


export default Autocomplete
