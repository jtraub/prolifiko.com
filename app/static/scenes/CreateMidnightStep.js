import React from 'react';
import { MidnightStepDetails } from '../components/StepDetails';
import Scene from '../components/Scene';

export default function CreateMidnightStep({ csrfToken, stepNumber }) {
    console.log('Rendering CreateMidnightStep');

    const stepDetails = props =>
        <MidnightStepDetails {...props} stepNumber={stepNumber}/>;

    return <Scene
        csrfToken={csrfToken}
        pages={[stepDetails]}
    />;
}
