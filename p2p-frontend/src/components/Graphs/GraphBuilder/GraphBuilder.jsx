import React, { useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import GraphBuilderForm from './GraphBuilderForm';
import GraphContainer from '../GraphContainer';
import useGraphData from '../../../hooks/useGraphData';

function GraphBuilder() {
  const [name, setName] = useState('');
  const [stat, setStat] = useState('');
  const [year, setYear] = useState('');
  const [gender, setGender] = useState('');
  const [ageGroup, setAgeGroup] = useState('');
  const [overlay, setOverlay] = useState(false);
  const [overlayUserTime, setOverlayUserTime] = useState(false);
  const [dataset, setDataset] = useState('competitive');

  const { apiUrl, resultType, result, graphTitle, fetchGraphData } = useGraphData();

  return (
    <Card>
      <CardContent>
        <Typography variant="h5">Build Your Own Graph or Stat</Typography>
        <GraphBuilderForm
          {...{ name, setName, stat, setStat, year, setYear, gender, setGender, ageGroup, setAgeGroup, overlay, setOverlay, overlayUserTime, setOverlayUserTime, dataset, setDataset }}
          onSubmit={(e) => { e.preventDefault(); fetchGraphData({ stat, name, year, gender, ageGroup, overlay, overlayUserTime, dataset }); }}
        />
        {resultType === 'graph' && apiUrl && <GraphContainer apiUrl={apiUrl} title={graphTitle} />}
      </CardContent>
    </Card>
  );
}

export default GraphBuilder;
