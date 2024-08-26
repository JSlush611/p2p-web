import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, Typography, CircularProgress, Box } from '@mui/material';
import Modal from './Modal';

function GraphContainer({ apiUrl, title }) {
  const [imageSrc, setImageSrc] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    console.log(process.env.REACT_APP_API_URI)
    axios.get(apiUrl, { responseType: 'blob' })
      .then(response => {
        const imgUrl = URL.createObjectURL(response.data);
        setImageSrc(imgUrl);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching the graph:', error);
        setError('Error fetching the graph.');
        setLoading(false);
      });
  }, [apiUrl]);

  return (
    <div>
      <Card
        elevation={4}
        sx={{
          cursor: 'pointer',
          height: '100%',  
          display: 'flex',
          flexDirection: 'column',
          '&:hover': {
            transform: 'scale(1.05)',
          },
          transition: 'transform 0.3s ease-in-out',
        }}
        onClick={() => setIsModalOpen(true)}
      >
        <CardContent sx={{ flexGrow: 1 }}>  
          {title && <Typography variant="h5" gutterBottom align="center">{title}</Typography>}
          {loading && (
            <Box display="flex" justifyContent="center" alignItems="center" sx={{ height: '250px' }}>
              <CircularProgress />
            </Box>
          )}
          {error && <Typography color="error">{error}</Typography>}
          {imageSrc && (
            <Box sx={{ height: '250px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <img src={imageSrc} alt="Graph" style={{ maxHeight: '100%', maxWidth: '100%', borderRadius: '4px' }} />
            </Box>
          )}
        </CardContent>
      </Card>

      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        imageSrc={imageSrc}
        title={title}
      />
    </div>
  );
}

export default GraphContainer;
