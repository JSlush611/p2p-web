import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import GraphBuilder from './GraphBuilder';

function GraphBuilderPage() {
  return (
    <Container maxWidth="md" style={{ marginTop: '20px' }}>
      <Typography variant="h4" align="center" gutterBottom>
        Build Your Own Graph
      </Typography>
      <Box mt={4}>
        <GraphBuilder />
      </Box>
    </Container>
  );
}

export default GraphBuilderPage;
