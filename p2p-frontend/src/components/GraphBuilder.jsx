import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, MenuItem, Card, CardContent, Typography, Box, Paper, FormControlLabel, Checkbox } from '@mui/material';
import GraphContainer from './GraphContainer';

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

const datasetOptions = [
  { value: 'competitive', label: 'Competitive' },
  { value: 'non-competitive', label: 'Non-Competitive' },
];

function GraphBuilder() {
  const [name, setName] = useState('');
  const [stat, setStat] = useState('');
  const [year, setYear] = useState('');  
  const [gender, setGender] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [overlay, setOverlay] = useState(false);
  const [overlayUserTime, setOverlayUserTime] = useState(false);
  const [apiUrl, setApiUrl] = useState(null);
  const [resultType, setResultType] = useState('');
  const [result, setResult] = useState(null);
  const [graphTitle, setGraphTitle] = useState('');
  const [dataset, setDataset] = useState('competitive');

  const buildApiUrl = (selectedStat) => {
    // let url = `${process.env.REACT_APP_API_URI}/api/user-${selectedStat.value}`;
    let url = `http://127.0.0.1:5000/api/user-${selectedStat.value}`;

    const params = new URLSearchParams();

    if (selectedStat.needYear) {
      params.append('name', name);
      params.append('year', year);
    } else if (selectedStat.needGender && selectedStat.needAgeGroup) {
      params.append('gender', gender);
      params.append('age_group', ageGroup);
      params.append('overlay', overlay);
      params.append('overlay_user_time', overlayUserTime);
      params.append('name', name);
    } else {
      params.append('name', name);
    }

    params.append('dataset', dataset);
    return `${url}?${params.toString()}`;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const selectedStat = statsOptions.find(option => option.value === stat);
      const constructedApiUrl = buildApiUrl(selectedStat);

      if (selectedStat.isGraph) {
        setApiUrl(constructedApiUrl);
        setResultType('graph');
        setGraphTitle(`${name}'s ${selectedStat.label}`);
      } else {
        const response = await axios.get(constructedApiUrl);
        setResultType('stat');
        setResult(response.data);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const renderStatResult = (data) => (
    <Paper elevation={3} sx={{ padding: '20px', textAlign: 'center', backgroundColor: '#f5f5f5', borderRadius: '8px' }}>
      <Typography variant="h6" gutterBottom>
        {`${data.name} - ${data.year}`}
      </Typography>
      <Typography variant="h4" color="primary">
        {`Position: ${data.position} / ${data.total_participants}`}
      </Typography>
      <Typography variant="body1">
        {`Age Group: ${data.age_group} | Participants in Age Group: ${data.total_participants_in_age_group}`}
      </Typography>
    </Paper>
  );

  return (
    <Card>
      <CardContent>
        <Typography variant="h5">Build Your Own Graph or Stat</Typography>
        <form onSubmit={handleSubmit}>
          <TextField label="Name" value={name} onChange={(e) => setName(e.target.value)} required fullWidth margin="normal" />
          <TextField select label="Statistic" value={stat} onChange={(e) => setStat(e.target.value)} required fullWidth margin="normal">
            {statsOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          {statsOptions.find(option => option.value === stat)?.needYear && (
            <TextField label="Year" type="number" value={year} onChange={(e) => setYear(e.target.value)} fullWidth margin="normal" />
          )}
          {statsOptions.find(option => option.value === stat)?.needGender && (
            <TextField select label="Gender" value={gender} onChange={(e) => setGender(e.target.value)} required fullWidth margin="normal">
              {genderOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          )}
          {statsOptions.find(option => option.value === stat)?.needAgeGroup && (
            <TextField select label="Age Group" value={ageGroup} onChange={(e) => setAgeGroup(e.target.value)} required fullWidth margin="normal">
              {ageGroupOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          )}
          {statsOptions.find(option => option.value === stat)?.canOverlay && (
            <>
              <FormControlLabel control={<Checkbox checked={overlay} onChange={(e) => setOverlay(e.target.checked)} />} label="Overlay with Overall Average Time" />
              <FormControlLabel control={<Checkbox checked={overlayUserTime} onChange={(e) => setOverlayUserTime(e.target.checked)} />} label="Overlay User's Time" />
            </>
          )}
          <TextField select label="Dataset" value={dataset} onChange={(e) => setDataset(e.target.value)} required fullWidth margin="normal">
            {datasetOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Generate Result
            </Button>
          </Box>
        </form>

        {resultType === 'graph' && apiUrl && (
          <Box mt={4}>
            <GraphContainer apiUrl={apiUrl} title={graphTitle} showDatasetToggle={false} />
          </Box>
        )}
        {resultType === 'stat' && result && (
          <Box mt={4}>
            {renderStatResult(result)}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default GraphBuilder;