const buildApiUrl = ({ selectedStat, name, year, gender, ageGroup, overlay, overlayUserTime, dataset }) => {
    if (!selectedStat) return '';

    let url = `${process.env.REACT_APP_API_URI}/api/user-${selectedStat.value}`;
    const params = new URLSearchParams();

    if (selectedStat.needYear) params.append('year', year);
    if (selectedStat.needGender) params.append('gender', gender);
    if (selectedStat.needAgeGroup) params.append('age_group', ageGroup);
    if (selectedStat.canOverlay) {
        params.append('overlay', overlay);
        params.append('overlay_user_time', overlayUserTime);
    }

    params.append('name', name);
    params.append('dataset', dataset);

    return `${url}?${params.toString()}`;
};

export { buildApiUrl };
