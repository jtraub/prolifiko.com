import React from 'react';
import StepDetails from '../components/StepDetails';
import Scene from '../components/Scene';

export default function CreateMidnightStep({ csrfToken, stepNumber }) {
    console.log('Rendering CreateMidnightStep');

    const stepDetails = props =>
        <StepDetails {...props} stepNumber={stepNumber}/>;

    return <Scene
        csrfToken={csrfToken}
        pages={[stepDetails]}
    />;
}
