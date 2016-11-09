import React from 'react';
import { CustomGoalDetails } from '../components/GoalDetails';
import GoalTarget  from '../components/GoalTarget';
import { CustomStepDetails } from '../components/StepDetails';
import StepDeadline from '../components/StepDeadline';
import Scene from '../components/Scene';

export default function CreateGoal({ csrfToken }) {
    console.log('Rendering CreateGoal');

    class CustomFirstStepDetails extends React.Component {
        static HEADING = CustomStepDetails.HEADING;

        render() {
            return <CustomStepDetails {...this.props} stepNumber={1} />;
        }
    }

    return <Scene
        csrfToken={csrfToken}
        pages={[
            CustomGoalDetails,
            GoalTarget,
            CustomFirstStepDetails,
            StepDeadline,
        ]}
        data={{ type: 'CUSTOM' }}
    />;
}
