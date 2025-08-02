import React, { useState, useEffect } from 'react';
import { Container, Typography, Grid, Avatar, Box, Paper, Link } from '@mui/material';

function AboutPage() {
  const calculateTimeLeft = () => {
    const nextRaceDate = new Date('August 1, 2025 07:20:00');
    const now = new Date();
    const difference = nextRaceDate - now;

    let timeLeft = {};

    if (difference > 0) {
      timeLeft = {
        days: Math.floor(difference / (1000 * 60 * 60 * 24)),
        hours: Math.floor((difference / (1000 * 60 * 60)) % 24),
        minutes: Math.floor((difference / 1000 / 60) % 60),
        seconds: Math.floor((difference / 1000) % 60),
      };
    }

    return timeLeft;
  };

  const [timeLeft, setTimeLeft] = useState(calculateTimeLeft());

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const timerComponents = Object.keys(timeLeft).map((interval) => {
    if (!timeLeft[interval]) {
      return null;
    }

    return (
      <Box key={interval} m={1}>
        <Paper elevation={3} sx={{ padding: '10px 20px', display: 'inline-block', minWidth: '80px' }}>
          <Typography variant="h4" color="primary">
            {timeLeft[interval]}
          </Typography>
          <Typography variant="caption">
            {interval.charAt(0).toUpperCase() + interval.slice(1)}
          </Typography>
        </Paper>
      </Box>
    );
  });

  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h5" align="center" gutterBottom>
        About the Point to La Pointe Data Visualization Tool
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
            Hello! I'm Jonathan Schluesche, a lifelong swimmer and dedicated computer science student.
            I've competed in swimming for most of my life, and recently participated in the Point to La Pointe swim.
            My experience as a swimmer, combined with my background in computer science, inspired me to create
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
      <Box mt={6} textAlign="center">
        <Typography variant="h6" align="center" gutterBottom>
          Time Left Until Next Year's Race
        </Typography>
        <Box display="flex" justifyContent="center" alignItems="center">
          {timerComponents.length ? timerComponents : <span>Time's up!</span>}
        </Box>
      </Box>

      {/* Footer section */}
      <Box mt={6} textAlign="center" component="footer">
        <Typography variant="body2">
          Check out my profiles and this project's source code:
        </Typography>
        <Box mt={2} display="flex" justifyContent="center" gap={3}>
          <Link href="https://github.com/JSlush611" target="_blank" rel="noopener" underline="hover">
            GitHub
          </Link>
          <Link href="https://www.linkedin.com/in/jonathan-schluesche-7a1a94252/" target="_blank" rel="noopener" underline="hover">
            LinkedIn
          </Link>
          <Link href="https://github.com/JSlush611/p2p-web" target="_blank" rel="noopener" underline="hover">
            Project Code
          </Link>
        </Box>
      </Box>
      <Box mt={6}></Box>
    </Container>
  );
}

export default AboutPage;