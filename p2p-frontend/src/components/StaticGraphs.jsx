import React from 'react';
import { Container, Grid } from '@mui/material';
import GraphContainer from './GraphContainer';

function StaticGraphs() {
  return (
    <Container maxWidth="lg" style={{ marginTop: '20px' }}>
      <Grid container spacing={4}>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/average-time-by-year'}
            title="Average Time"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/median-time-by-year'}
            title="Median Time"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/participation-by-year'}
            title="Overall Participation"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/average-time-by-age-group-and-year'}
            title="Average Time by Age Group"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/participation-by-region'}
            title="Regional Participation"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/time-percentiles-by-year'}
            title="Time Percentiles"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/gender-distribution-by-year'}
            title="Gender Distribution"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/top-10-fastest-swimmers'}
            title="Top 10 Fastest Swimmers"
          />
        </Grid>
        {/* <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'process.env.REACT_APP_API_URI' + '/api/age-vs-time-distribution'}
            title="Age vs Time"
          />
        </Grid> */}
        <Grid item xs={12} sm={6} md={4}>
          <GraphContainer
            apiUrl={'http://127.0.0.1:5000' + '/api/participation-by-age-group'}
            title="Age Group Participation"
          />
        </Grid>
      </Grid>
    </Container>
  );
}

export default StaticGraphs;
