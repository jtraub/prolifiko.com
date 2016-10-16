import React from 'react';
import StepDetails from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateStep({ csrfToken }) {
    console.log('Rendering CreateStep');

    const stepDetails = props =>
        <StepDetails {...props} stepNumber={window.DATA.stepNumber}/>;

    return <Scene
        csrfToken={csrfToken}
        pages={[stepDetails, StepDeadline]}
    />;
}
