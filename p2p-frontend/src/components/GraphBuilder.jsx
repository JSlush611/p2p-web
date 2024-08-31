import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, MenuItem, Card, CardContent, Typography, Box, Paper, FormControlLabel, Checkbox } from '@mui/material';

const statsOptions = [
  { value: 'time-by-year', label: 'Time Over Years', needYear: false },
  { value: 'percentile-by-year', label: 'Percentile Over Years', needYear: false },
  { value: 'position-in-year', label: 'Position in Specific Year', needYear: true },
  { value: 'average-time-gender-age-group-and-year', label: 'Average Time by Gender/Age Group', needYear: false, needGender: true, needAgeGroup: true, canOverlay: true },
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

function GraphBuilder() {
  const [name, setName] = useState('');
  const [stat, setStat] = useState('');
  const [year, setYear] = useState('');  
  const [gender, setGender] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [overlay, setOverlay] = useState(false);
  const [overlayUserTime, setOverlayUserTime] = useState(false); // Add state for the user time overlay
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
  
    try {
      const selectedStat = statsOptions.find(option => option.value === stat);
      let apiUrl = `${process.env.REACT_APP_API_URI}/api/user-${stat}`;
      
      if (selectedStat.needYear) {
        apiUrl += `?name=${encodeURIComponent(name)}&year=${year}`;
      } else if (selectedStat.needGender && selectedStat.needAgeGroup) {
          apiUrl += `?gender=${gender}&age_group=${ageGroup}&overlay=${overlay}&overlay_user_time=${overlayUserTime}&name=${encodeURIComponent(name)}`;
      } else {
          apiUrl += `?name=${encodeURIComponent(name)}`;
      }
  
      const response = await axios.get(apiUrl, { responseType: 'blob' });
  
      if (response.headers['content-type'].includes('image')) {
        const imgUrl = URL.createObjectURL(response.data);
        setResult({ type: 'image', content: imgUrl });
      } else {
        const reader = new FileReader();
        reader.onload = () => {
          setResult({ type: 'text', content: JSON.parse(reader.result) });
        };
        reader.readAsText(response.data);
      }
    } catch (err) {
      console.error(err);
      setError('Error generating result. Please try again.');
    } finally {
      setLoading(false);
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
        <Typography variant="h5">Build Your Own Graph</Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
            fullWidth
            margin="normal"
          />
          <TextField
            select
            label="Statistic"
            value={stat}
            onChange={(e) => setStat(e.target.value)}
            required
            fullWidth
            margin="normal"
          >
            {statsOptions.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          {statsOptions.find(option => option.value === stat)?.needYear && (
            <TextField
              label="Year"
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              fullWidth
              margin="normal"
            />
          )}
          {statsOptions.find(option => option.value === stat)?.needGender && (
            <TextField
              select
              label="Gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              required
              fullWidth
              margin="normal"
            >
              {genderOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          )}
          {statsOptions.find(option => option.value === stat)?.needAgeGroup && (
            <TextField
              select
              label="Age Group"
              value={ageGroup}
              onChange={(e) => setAgeGroup(e.target.value)}
              required
              fullWidth
              margin="normal"
            >
              {ageGroupOptions.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </TextField>
          )}
          {statsOptions.find(option => option.value === stat)?.canOverlay && (
            <>
              <FormControlLabel
                control={<Checkbox checked={overlay} onChange={(e) => setOverlay(e.target.checked)} />}
                label="Overlay with Overall Average Time"
              />
              <FormControlLabel
                control={<Checkbox checked={overlayUserTime} onChange={(e) => setOverlayUserTime(e.target.checked)} />}
                label="Overlay User's Time"
              />
            </>
          )}
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Generate Result
            </Button>
          </Box>
        </form>
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && result.type === 'image' && (
          <Box mt={2}>
            <img src={result.content} alt="Custom Graph" style={{ width: '100%', borderRadius: '4px' }} />
          </Box>
        )}
        {result && result.type === 'text' && (
          <Box mt={2}>
            {renderStatResult(result.content)}
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default GraphBuilder;