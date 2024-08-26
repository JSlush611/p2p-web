import React from 'react';
import { Container, Typography, Grid, Avatar, Box } from '@mui/material';

function AboutPage() {
  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h5" align="center" gutterBottom>
        About Point to La Pointe Data Visualization Tool
      </Typography>
      <Grid container spacing={4} alignItems="center" justifyContent="center">
        <Grid item xs={12} sm={4}>
          <Avatar
            alt="Jonathan Schluesche"
            src="/headshot.jpeg"
            sx={{ width: 150, height: 150, margin: 'auto' }}
          />
        </Grid>
        <Grid item xs={12} sm={8}>
          <Typography variant="body1" align="center">
            Hello! I'm Jonathan Schluesche, a long time swimmer and a dedicated computer science student. 
            I have swam competivily for most of my life, and recently competed in Point to La Pointe. My 
            experience as a swimmer, combined with my background in computer science, inspired me to create 
            this data visualization tool. I hope it helps fellow swimmers and enthusiasts explore the rich 
            history and data of this event.
          </Typography>
        </Grid>
      </Grid>
      <Box mt={4}>
        <Typography variant="body1" align="center">
          This tool allows you to visualize swim race data from Point to La Pointe over the years. 
          You can explore various statistics such as average times, median times, participation 
          rates, and much more. Additionally, you can build your own custom graphs to analyze specific 
          data points.
        </Typography>
      </Box>
    </Container>
  );
}

export default AboutPage;
