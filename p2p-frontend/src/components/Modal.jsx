import React from 'react';
import { Dialog, DialogTitle, DialogContent, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';
import Plot from 'react-plotly.js';

function Modal({ isOpen, onClose, graphData, graphLayout, title }) {
  return (
    <Dialog open={isOpen} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {title}
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{
            position: 'absolute',
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Plot
          data={graphData}
          layout={graphLayout}
          style={{ width: '100%', height: '100%' }}
          useResizeHandler
        />
      </DialogContent>
    </Dialog>
  );
}

export default Modal;
