import React from 'react';
import { Container, Typography, Box } from '@mui/material';

function ThankYouPage() {
  return (
    <Container maxWidth="sm">
      <Box mt={5}>
        <Typography variant="h4" align="center" gutterBottom>
          Thank You!
        </Typography>
        <Typography variant="body1" align="center">
          Your request has been submitted successfully. We appreciate your feedback and will get back to you if necessary.
        </Typography>
      </Box>
    </Container>
  );
}

export default ThankYouPage;
