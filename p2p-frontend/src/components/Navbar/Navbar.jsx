import React from 'react';
import { AppBar, Toolbar, Typography, Button, Container } from '@mui/material';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <AppBar position="static">
      <Container>
        <Toolbar>
          <Typography variant="h6" style={{ flexGrow: 1 }}>
            Point to La Pointe
          </Typography>
          <Button color="inherit" component={Link} to="/">
            About
          </Button>
          <Button color="inherit" component={Link} to="/graphs">
            Static Graphs
          </Button>
          <Button color="inherit" component={Link} to="/build-graph">
            Build Graph
          </Button>
          <Button color="inherit" component={Link} to="/suggestions">
            Submit Suggestions
          </Button>
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default Navbar;
