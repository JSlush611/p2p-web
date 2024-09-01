import React, { useState, useEffect } from 'react';
import emailjs from 'emailjs-com';
import { TextField, Button, MenuItem, Box, Typography, Container } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import ReCAPTCHA from 'react-google-recaptcha';

const requestTypes = [
  { value: 'feature', label: 'New Feature Request' },
  { value: 'visualization', label: 'New Visualization Request' },
  { value: 'misc', label: 'Miscellaneous Request' },
];

function ContactForm() {
  const [requestType, setRequestType] = useState('');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const [captchaToken, setCaptchaToken] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    emailjs.init(process.env.REACT_APP_EMAILJS_PUBLIC_KEY);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!captchaToken) {
      alert('Please complete the CAPTCHA');
      return;
    }
  
    emailjs.sendForm(
      process.env.REACT_APP_EMAIL_JS_SERVICE_ID,
      process.env.REACT_APP_EMAIL_JS_TEMPLATE_ID,
      e.target,
      process.env.REACT_APP_EMAILJS_PUBLIC_KEY,
    ).then(
      (result) => {
        console.log(result.text);
        alert('Message sent successfully!');
        navigate('/thank-you');  
      },
      (error) => {
        console.log(error.text);
        alert('Failed to send message.');
      }
    );
  };

  const onCaptchaChange = (token) => {
    setCaptchaToken(token);
  };

  return (
    <Container maxWidth="sm">
      <Box mt={5}>
        <Typography variant="h5" align="center">Submit Your Request</Typography>
        <form onSubmit={handleSubmit}>
          <TextField
            select
            label="Request Type"
            value={requestType}
            onChange={(e) => setRequestType(e.target.value)}
            fullWidth
            required
            margin="normal"
            name="request_type"
          >
            {requestTypes.map((option) => (
              <MenuItem key={option.value} value={option.value}>
                {option.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Name"
            fullWidth
            required
            margin="normal"
            value={name}
            onChange={(e) => setName(e.target.value)}
            name="from_name"
          />
          <TextField
            label="Email"
            type="email"
            fullWidth
            required
            margin="normal"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            name="reply_to"
          />
          <TextField
            label="Message"
            fullWidth
            required
            multiline
            rows={4}
            margin="normal"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            name="message"
          />
          <Box mt={2}>
            <ReCAPTCHA
              sitekey={process.env.REACT_APP_RECAPTCHA_SITE_KEY}
              onChange={onCaptchaChange}
            />
          </Box>
          <Box mt={2}>
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Send Request
            </Button>
          </Box>
        </form>
      </Box>
    </Container>
  );
}

export default ContactForm;