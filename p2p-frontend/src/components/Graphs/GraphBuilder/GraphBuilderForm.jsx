import React from 'react';
import { TextField, MenuItem, FormControlLabel, Checkbox, Button, Box } from '@mui/material';
import { statsOptions, genderOptions, ageGroupOptions } from '../../../utils/statsOptions';

const GraphBuilderForm = ({
    name, setName,
    stat, setStat,
    year, setYear,
    gender, setGender,
    ageGroup, setAgeGroup,
    overlay, setOverlay,
    overlayUserTime, setOverlayUserTime,
    dataset, setDataset,
    onSubmit
}) => {
    const selectedStat = statsOptions.find(option => option.value === stat);

    return (
        <form onSubmit={onSubmit}>
            {/* Name Input */}
            <TextField
                label="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                fullWidth
                margin="normal"
            />

            {/* Statistic Selection */}
            <TextField
                select
                label="Statistic"
                value={stat}
                onChange={(e) => setStat(e.target.value)}
                required
                fullWidth
                margin="normal"
            >
                {statsOptions.map(option => (
                    <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                ))}
            </TextField>

            {/* Year Input (Only if Required) */}
            {selectedStat?.needYear && (
                <TextField
                    label="Year"
                    type="number"
                    value={year}
                    onChange={(e) => setYear(e.target.value)}
                    required
                    fullWidth
                    margin="normal"
                />
            )}

            {/* Gender Selection (Only if Required) */}
            {selectedStat?.needGender && (
                <TextField
                    select
                    label="Gender"
                    value={gender}
                    onChange={(e) => setGender(e.target.value)}
                    required
                    fullWidth
                    margin="normal"
                >
                    {genderOptions.map(option => (
                        <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                    ))}
                </TextField>
            )}

            {/* Age Group Selection (Only if Required) */}
            {selectedStat?.needAgeGroup && (
                <TextField
                    select
                    label="Age Group"
                    value={ageGroup}
                    onChange={(e) => setAgeGroup(e.target.value)}
                    required
                    fullWidth
                    margin="normal"
                >
                    {ageGroupOptions.map(option => (
                        <MenuItem key={option.value} value={option.value}>{option.label}</MenuItem>
                    ))}
                </TextField>
            )}

            {/* Overlay Options (Only if Supported by Selected Stat) */}
            {selectedStat?.canOverlay && (
                <>
                    <FormControlLabel
                        control={<Checkbox checked={overlay} onChange={(e) => setOverlay(e.target.checked)} />}
                        label="Overlay with Overall Average Time"
                    />
                    <FormControlLabel
                        control={<Checkbox checked={overlayUserTime} onChange={(e) => setOverlayUserTime(e.target.checked)} />}
                        label="Overlay User's Time"
                    />
                </>
            )}

            {/* Dataset Selection */}
            <TextField
                select
                label="Dataset"
                value={dataset}
                onChange={(e) => setDataset(e.target.value)}
                required
                fullWidth
                margin="normal"
            >
                <MenuItem value="competitive">Competitive</MenuItem>
                <MenuItem value="non-competitive">Non-Competitive</MenuItem>
            </TextField>

            {/* Submit Button */}
            <Box mt={2}>
                <Button type="submit" variant="contained" color="primary" fullWidth>
                    Generate Result
                </Button>
            </Box>
        </form>
    );
};

export default GraphBuilderForm;
