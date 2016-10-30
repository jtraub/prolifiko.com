import React from 'react';
import CreateFiveDayChallenge from '../CreateFiveDayChallenge';
import { MidnightStepDetails } from '../../components/StepDetails';
import { FiveDayChallengeDetails } from '../../components/GoalDetails';
import Textarea from '../../components/Textarea';
import { mount } from 'enzyme';

describe('<CreateFiveDayChallenge/>', () => {
    let wrapper;

    it('prompts for goal and step details', () => {
        wrapper = mount(<CreateFiveDayChallenge csrfToken="foo"/>);

        // Page 1 - FiveDayChallengeGoal

        const goalDetails = wrapper.find(FiveDayChallengeDetails);
        expect(goalDetails.isEmpty()).toBe(false);

        const goalDescription = goalDetails.find(Textarea).find('textarea');

        expect(goalDescription.isEmpty()).toBe(false);

        goalDescription.simulate('change', { target: { value: 'A goal description' }});

        // Next page

        wrapper.find('#next').simulate('click');
        expect(wrapper.find(FiveDayChallengeDetails).isEmpty()).toBe(true);
        expect(wrapper.find('#prev').isEmpty()).toBe(false);
        expect(wrapper.find('#next').isEmpty()).toBe(true);
        expect(wrapper.find('#submit').isEmpty()).toBe(false);

        // Page 2 - Step Details

        const stepDetails = wrapper.find(MidnightStepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepDescription.isEmpty()).toBe(false);

        stepDescription.simulate('change', { target: { value: 'A step description' }});

        expect(wrapper.find('input[name="goal_name"]').prop('value')).toBe('Five Day Challenge');
        expect(wrapper.find('input[name="goal_description"]').prop('value')).toBe('A goal description');
        expect(wrapper.find('input[name="step_name"]').prop('value')).toBe('First Step');
        expect(wrapper.find('input[name="step_description"]').prop('value')).toBe('A step description');
    });
});
