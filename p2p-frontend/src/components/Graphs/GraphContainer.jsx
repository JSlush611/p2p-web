import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, Box, Button, Table, TableContainer, TableHead, TableRow, TableCell, TableBody, Paper } from '@mui/material';
import Plot from 'react-plotly.js';

function GraphContainer({ apiUrl, title, showDatasetToggle = true }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [viewMode, setViewMode] = useState('graph');
  const [dataset, setDataset] = useState('competitive');

  useEffect(() => {
    const fetchData = () => {
      const separator = apiUrl.includes('?') ? '&' : '?';
      const apiUrlWithDataset = `${apiUrl}${separator}dataset=${dataset}`;

      axios.get(apiUrlWithDataset)
        .then(response => {
          setData(response.data);
          setLoading(false);
          setError(null);
        })
        .catch(err => {
          console.error('Error fetching the data:', err);
          if (err.response && err.response.data) {
            setError(err.response.data);
          } else {
            setError({ error: true, message: 'Error fetching the data.' });
          }
          setLoading(false);
        });
    };

    fetchData();
  }, [apiUrl, dataset]);

  const toggleViewMode = () => {
    setViewMode(viewMode === 'graph' ? 'table' : 'graph');
  };

  const toggleDataset = () => {
    setDataset((prev) => (prev === 'competitive' ? 'non-competitive' : 'competitive'));
  };

  const renderStatResult = (data) => {
    if (data.error) {
      return (
        <Paper
          elevation={3}
          sx={{
            padding: '20px',
            marginTop: '20px',
            textAlign: 'center',
            backgroundColor: '#f5f5f5',
            borderRadius: '8px',
          }}
        >
          <Typography
            variant="h6"
            gutterBottom
            color="error"
            sx={{ fontWeight: 'bold' }}
          >
            {data.message}
          </Typography>
          {data.suggestion && (
            <Typography variant="body1" sx={{ marginTop: '10px' }}>
              {data.suggestion}
            </Typography>
          )}
        </Paper>
      );
    }

    return (
      <Paper
        elevation={3}
        sx={{
          padding: '20px',
          marginTop: '20px',
          textAlign: 'center',
          backgroundColor: '#f5f5f5',
          borderRadius: '8px',
        }}
      >
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
  };

  return (
    <div>
      <Card
        elevation={4}
        sx={{
          height: '500px',
          display: 'flex',
          flexDirection: 'column',
        }}>
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
                  <Button
                    onClick={toggleDataset}
                    variant="outlined"
                    size="small"
                    sx={{ padding: '4px 8px', minWidth: 'unset', textTransform: 'none', fontSize: '0.8rem' }}
                  >
                    {dataset === 'competitive' ? 'Non-Comp Data' : 'Comp Data'}
                  </Button>
                )}
                {data && data.table && (
                  <Button
                    onClick={toggleViewMode}
                    variant="outlined"
                    size="small"
                    sx={{ padding: '4px 8px', minWidth: 'unset', textTransform: 'none', fontSize: '0.8rem' }}
                  >
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

          {!loading && error && error.error && (
            <Paper
              elevation={3}
              sx={{
                padding: '20px',
                marginTop: '20px      ',
                textAlign: 'center',
                backgroundColor: '#f5f5f5',
                borderRadius: '8px',
              }}
            >
              <Typography
                variant="h6"
                gutterBottom
                color="error"
                sx={{ fontWeight: 'bold' }}
              >
                {error.message}
              </Typography>
              {error.suggestion && (
                <Typography variant="body1" sx={{ marginTop: '10px' }}>
                  {error.suggestion}
                </Typography>
              )}
            </Paper>
          )}

          {!loading && !error && data && (
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
              {!data.graph && !data.table && renderStatResult(data)}
            </>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default GraphContainer;
