import React from 'react';
import { CustomStepDetails } from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateStep({ csrfToken, stepNumber }) {
    console.log('Rendering CreateStep');

    const stepDetails = props =>
        <CustomStepDetails {...props} stepNumber={stepNumber} />;

    return <Scene
        csrfToken={csrfToken}
        pages={[stepDetails, StepDeadline]}
    />;
}
