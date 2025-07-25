const statsOptions = [
    { value: 'time-by-year', label: 'Time Over Years', needYear: false, isGraph: true },
    { value: 'percentile-by-year', label: 'Percentile Over Years', needYear: false, isGraph: true },
    { value: 'position-in-year', label: 'Position in Specific Year', needYear: true, isGraph: false },
    { value: 'average-time-gender-age-group-and-year', label: 'Average Time by Gender/Age Group', needYear: false, needGender: true, needAgeGroup: true, canOverlay: true, isGraph: true },
];

const genderOptions = [
    { value: 'M', label: 'Male' },
    { value: 'F', label: 'Female' },
];

const ageGroupOptions = [
    { value: '13-19', label: '13-19' },
    { value: '20-24', label: '20-24' },
    { value: '25-29', label: '25-29' },
    { value: '30-34', label: '30-34' },
    { value: '35-39', label: '35-39' },
    { value: '40-44', label: '40-44' },
    { value: '45-49', label: '45-49' },
    { value: '50-54', label: '50-54' },
    { value: '55-59', label: '55-59' },
    { value: '60-64', label: '60-64' },
    { value: '65-69', label: '65-69' },
    { value: '70+', label: '70+' },
];

export { statsOptions, genderOptions, ageGroupOptions };
