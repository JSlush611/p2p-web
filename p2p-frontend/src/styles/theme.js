import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#00796b',
    },
    secondary: {
      main: '#ff4081', 
    },
    background: {
      default: '#f4f6f8', 
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
    h5: {
      fontWeight: 700,
      color: '#00796b', 
    },
  },
});

export default theme;
