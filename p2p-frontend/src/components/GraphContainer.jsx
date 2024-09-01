import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, Box } from '@mui/material';
import Plot from 'react-plotly.js';

function GraphContainer({ apiUrl, title }) {
  const [plotData, setPlotData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    console.log(apiUrl);
    axios.get(apiUrl)
      .then(response => {
        setPlotData(JSON.parse(response.data));
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching the graph:', error);
        setError('Error fetching the graph.');
        setLoading(false); 
      });
  }, [apiUrl]);

  return (
    <div>
      <Card
        elevation={4}
        sx={{
          height: '100%',  
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <CardContent sx={{ flexGrow: 1 }}>  
          {title && <Typography variant="h5" gutterBottom align="center">{title}</Typography>}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" sx={{ height: '250px' }}>
              <CircularProgress />
            </Box>
          )}
          {error && <Typography color="error">{error}</Typography>}
          {plotData && (
            <Plot
              data={plotData.data}
              layout={plotData.layout}
              style={{ width: "100%", height: "100%" }}
              useResizeHandler
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default GraphContainer;
