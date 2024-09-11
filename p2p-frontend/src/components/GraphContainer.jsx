import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, Box, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import Plot from 'react-plotly.js';

function GraphContainer({ apiUrl, title, showDatasetToggle = true }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('graph');
  const [dataset, setDataset] = useState('competitive'); 

  useEffect(() => {
    const fetchData = () => {
      // Construct the API URL with the dataset parameter
      const separator = apiUrl.includes('?') ? '&' : '?';
      const apiUrlWithDataset = `${apiUrl}${separator}dataset=${dataset}`;

      axios.get(apiUrlWithDataset)
        .then(response => {
          setData(response.data);
          setLoading(false);
        })
        .catch(error => {
          console.error('Error fetching the data:', error);
          setError('Error fetching the data.');
          setLoading(false); 
        });
    };

    fetchData();
  }, [apiUrl, dataset]); // Add `dataset` to the dependency array

  const toggleViewMode = () => {
    setViewMode(viewMode === 'graph' ? 'table' : 'graph');
  };

  const toggleDataset = () => {
    setDataset((prevDataset) => (prevDataset === 'competitive' ? 'non-competitive' : 'competitive'));
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
    <div>
      <Card
        elevation={4}
        sx={{
          height: '500px',  
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
          {title && (
            <Box 
              display="flex" 
              justifyContent="space-between" 
              alignItems="center" 
              sx={{ minHeight: '60px' }}  
            >
              <Typography 
                variant="h6" 
                gutterBottom 
                align="center" 
                sx={{ fontSize: '1rem', flex: 1, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }} 
              >
                {title}
              </Typography>
              <Box sx={{ display: 'flex', gap: 1 }}>
                {showDatasetToggle && (
                  <Button onClick={toggleDataset} variant="outlined" size="small" sx={{ padding: '4px 8px', minWidth: 'unset', textTransform: 'none', fontSize: '0.8rem' }}>
                    {dataset === 'competitive' ? 'Non-Comp Data' : 'Comp Data'}
                  </Button>
                )}
                {data && data.table && (
                  <Button onClick={toggleViewMode} variant="outlined" size="small" sx={{ padding: '4px 8px', minWidth: 'unset', textTransform: 'none', fontSize: '0.8rem' }}>
                    {viewMode === 'graph' ? 'Table' : 'Graph'}
                  </Button>
                )}
              </Box>
            </Box>
          )}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" sx={{ flexGrow: 1 }}>
              <CircularProgress size={24} />
            </Box>
          )}
          {error && <Typography color="error">{error}</Typography>}
          {data && (
            <>
              {viewMode === 'graph' && data.graph && (
                <Box sx={{ flexGrow: 1, display: 'flex' }}>
                  <Plot
                    data={JSON.parse(data.graph).data || []}
                    layout={JSON.parse(data.graph).layout || {}}
                    style={{ width: "100%", height: "100%" }}
                    useResizeHandler
                  />
                </Box>
              )}
              {viewMode === 'table' && data.table && (
                <TableContainer component={Paper} sx={{ maxHeight: '400px', overflowY: 'auto' }}>
                  <Table stickyHeader>
                    <TableHead>
                      <TableRow>
                        {Object.keys(data.table[0] || {}).map((key) => (
                          <TableCell key={key}>{key}</TableCell>
                        ))}
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {data.table.map((row, index) => (
                        <TableRow key={index}>
                          {Object.values(row).map((value, cellIndex) => (
                            <TableCell key={cellIndex}>{value}</TableCell>
                          ))}
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              )}
              {!data.graph && renderStatResult(data)}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default GraphContainer;
// Testing the update!