import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, MenuItem, Card, CardContent, Typography, Box } from '@mui/material';

const statsOptions = [
  { value: 'time-by-year', label: 'Time Over Years' },
  { value: 'percentile-by-year', label: 'Percentile Over Years' },
  { value: 'position-in-year', label: 'Position in Specific Year' },
];

function GraphBuilder() {
  const [name, setName] = useState('');
  const [stat, setStat] = useState('');
  const [year, setYear] = useState('');  
  const [imageSrc, setImageSrc] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      let apiUrl = `${process.env.REACT_APP_API_URI}/api/user-${stat}?name=${name}`;
      if (stat === 'position-in-year') {
        apiUrl += `&year=${year}`;  // Only use year for position
      }
      
      const response = await axios.get(apiUrl, { responseType: 'blob' });
      const imgUrl = URL.createObjectURL(response.data);
      setImageSrc(imgUrl);
    } catch (err) {
      console.error(err);
      setError('Error generating graph. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
          {stat === 'position-in-year' && (
            <TextField
              label="Year"
              type="number"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              required
              fullWidth
              margin="normal"
            />
          )}
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Generate Graph
            </Button>
          </Box>
        </form>
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {imageSrc && (
          <Box mt={2}>
            <img src={imageSrc} alt="Custom Graph" style={{ width: '100%', borderRadius: '4px' }} />
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

export default GraphBuilder;
