import React from 'react';
import { Dialog, DialogTitle, DialogContent, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

function Modal({ isOpen, onClose, imageSrc, title }) {
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
        <img src={imageSrc} alt={title} style={{ width: '100%', borderRadius: '4px' }} />
      </DialogContent>
    </Dialog>
  );
}

export default Modal;
