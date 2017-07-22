import React from 'react'
import Autocomplete from 'WagtailAutocomplete/Autocomplete'
import classNames from 'classnames'
import DatePicker from 'react-datepicker'


export function AutocompleteInput({
	handleFilterChange,
	filterValues,
	label,
	filter,
	type,
	isSingle,
}) {
	return (
		<div>
			{label}:
			{' '}
			<Autocomplete
				type={type}
				name={filter}
				canCreate={false}
				isSingle={isSingle}
				value={filterValues[filter]}
				onChange={handleFilterChange.bind(null, filter)}
				fetchInitialValues={true}
				apiBase="/autocomplete/"
				controlled={true}
			/>
		</div>
	)
}


export function RadioPillInput({
	handleFilterChange,
	filterValues,
	label,
	filter,
	options,
}) {
	return (
		<div>
			{label}:
			{' '}

			<span className="radio-pill">
				{options.map(option => (
					<button
						key={option.value}
						value={option.value}
						type="button"
						onClick={handleFilterChange.bind(null, filter)}
						className={classNames(
							'radio-pill__item',
							{ 'radio-pill__item--selected': filterValues[filter] === option.value }
						)}
					>
						{option.label}
					</button>
				))}
			</span>
		</div>
	)
}


RadioPillInput.defaultProps = {
	options: [
		{ label: 'Unknown', value: 'NOTHING' },
		{ label: 'Yes', value: 'JUST_TRUE' },
		{ label: 'No', value: 'JUST_FALSE' },
	],
}


export function TextInput({ handleFilterChange, filterValues, label, filter }) {
	const value = filterValues[filter] || ''
	return (
		<div>
			{label}:
			{' '}
			<input
				type="text"
				onChange={handleFilterChange.bind(null, filter)}
				value={value}
				className={classNames(
					'filter-text-input',
					{ 'filter-text-input--has-input': value.length > 0 }
				)}
			/>
		</div>
	)
}


export function BoolInput({ handleFilterChange, filterValues, label, filter }) {
	return (
		<div>
			{label}:
			{' '}
			<input
				type="checkbox"
				onChange={handleFilterChange.bind(null, filter)}
				value={filterValues[filter] || false}
			/>
		</div>
	)
}


export function ChoiceInput({ handleFilterChange, filterValues, label, filter, choices }) {
	return (
		<div>
			{label}:
			{' '}
			<select
				onChange={handleFilterChange.bind(null, filter)}
				value={filterValues[filter] || ''}
			>
				<option value=""></option>
				{choices.map(choice => (
					<option
						key={choice.value}
						value={choice.value}
					>
						{choice.label}
					</option>
				))}
			</select>
		</div>
	)
}


export function DateRangeInput({ handleFilterChange, filterValues, label, filter_lower, filter_upper }) {
	return (
		<div>
			{label}
			{' '}
			<span className="filters__date-picker">
				<DatePicker
					onChange={handleFilterChange.bind(null, filter_lower)}
					selected={filterValues[filter_lower] || ''}
					isClearable={true}
					className={classNames(
						'filter-date-picker',
						{ 'filter-date-picker--has-input': !!filterValues[filter_lower] }
					)}
				/>
			</span>
			{' '}
			and
			{' '}
			<span className="filters__date-picker">
				<DatePicker
					onChange={handleFilterChange.bind(null, filter_upper)}
					selected={filterValues[filter_upper] || ''}
					isClearable={true}
					className={classNames(
						'filter-date-picker',
						{ 'filter-date-picker--has-input': !!filterValues[filter_upper] }
					)}
				/>
			</span>
		</div>
	)
}