import { useState } from 'react';
import axios from 'axios';
import { buildApiUrl } from '../utils/apiUtils';
import { statsOptions } from '../utils/statsOptions';

const useGraphData = () => {
    const [apiUrl, setApiUrl] = useState(null);
    const [resultType, setResultType] = useState('');
    const [result, setResult] = useState(null);
    const [graphTitle, setGraphTitle] = useState('');

    const fetchGraphData = async ({ stat, name, year, gender, ageGroup, overlay, overlayUserTime, dataset }) => {
        try {
            const selectedStat = statsOptions.find(option => option.value === stat);
            const constructedApiUrl = buildApiUrl({ selectedStat, name, year, gender, ageGroup, overlay, overlayUserTime, dataset });

            if (selectedStat.isGraph) {
                setApiUrl(constructedApiUrl);
                setResultType('graph');
                setGraphTitle(`${name}'s ${selectedStat.label}`);
                setResult(null);
            } else {
                const response = await axios.get(constructedApiUrl);
                setResultType('stat');
                setResult(response.data);
            }
        } catch (err) {
            console.error(err);
            setResultType('stat');
            setResult({ error: true, message: 'Error fetching the data.' });
        }
    };

    return { apiUrl, resultType, result, graphTitle, fetchGraphData };
};

export default useGraphData;
