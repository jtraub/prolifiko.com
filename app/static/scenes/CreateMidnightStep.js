import React from 'react';
import StepDetails from '../components/StepDetails';
import Scene from '../components/Scene';

export default function CreateMidnightStep({ csrfToken }) {
    return <Scene
        csrfToken={csrfToken}
        pages={[StepDetails]}
    />;
}
