import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, Box, Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
// eslint-disable-next-line
import Plot from 'react-plotly.js';

function GraphContainer({ apiUrl, title }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('graph'); 

  useEffect(() => {
    axios.get(apiUrl)
      .then(response => {
        setData(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching the data:', error);
        setError('Error fetching the data.');
        setLoading(false); 
      });
  }, [apiUrl]);

  const toggleViewMode = () => {
    setViewMode(viewMode === 'graph' ? 'table' : 'graph');
  };

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
            <Box display="flex" justifyContent="space-between" alignItems="center">
              <Typography variant="h5" gutterBottom align="center">{title}</Typography>
              {data && data.table && (
                <Button onClick={toggleViewMode} variant="contained">
                  {viewMode === 'graph' ? 'View Table' : 'View Graph'}
                </Button>
              )}
            </Box>
          )}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" sx={{ flexGrow: 1 }}>
              <CircularProgress />
            </Box>
          )}
          {error && <Typography color="error">{error}</Typography>}
          {data && viewMode === 'graph' && data.graph && (
            <Box sx={{ flexGrow: 1, display: 'flex' }}>
              <Plot
                data={data.graph ? JSON.parse(data.graph).data : []}
                layout={data.graph ? JSON.parse(data.graph).layout : {}}
                style={{ width: "100%", height: "100%" }}
                useResizeHandler
              />
            </Box>
          )}
          {data && viewMode === 'table' && data.table && (
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
        </CardContent>
      </Card>
    </div>
  );
}

export default GraphContainer;