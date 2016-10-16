import React from 'react';
import StepDetails from '../components/StepDetails';
import Scene from '../components/Scene';

export default function CreateMidnightStep({ csrfToken }) {
    const stepDetails = props =>
        <StepDetails {...props} stepNumber={window.DATA.stepNumber}/>;

    return <Scene
        csrfToken={csrfToken}
        pages={[stepDetails]}
    />;
}
