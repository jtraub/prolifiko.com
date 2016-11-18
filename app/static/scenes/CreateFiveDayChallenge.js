import React from 'react';
import { MidnightStepDetails } from '../components/StepDetails';
import { FiveDayChallengeDetails } from '../components/GoalDetails';
import Scene from '../components/Scene';

export default function CreateFiveDayChallenge({ csrfToken }) {
    console.log('Rendering CreateFiveDayChallenge');

    class StepDetailsWrapper extends React.Component {
        static HEADING = MidnightStepDetails.HEADING;

        render() {
            return <MidnightStepDetails {...this.props} stepNumber={1} />;
        }
    }

    return <Scene
        csrfToken={csrfToken}
        pages={[
            FiveDayChallengeDetails,
            StepDetailsWrapper,
        ]}
        data={{ type: 'FIVE_DAY_CHALLENGE' }}
    />;
}
