import React from 'react';
import CreateFiveDayChallenge from '../CreateFiveDayChallenge';
import StepDetails from '../../components/StepDetails';
import GoalDetails from '../../components/GoalDetails';
import Textarea from '../../components/Textarea';
import { mount } from 'enzyme';

describe('<CreateFiveDayChallenge/>', () => {
    let wrapper;

    it('prompts for goal and step details', () => {
        wrapper = mount(<CreateFiveDayChallenge csrfToken="foo"/>);

        // Page 1 - GoalDetails

        const goalDetails = wrapper.find(GoalDetails);
        expect(goalDetails.isEmpty()).toBe(false);

        const goalName = goalDetails.find('input[name="goalName"]');
        const goalDescription = goalDetails.find(Textarea).find('textarea');

        expect(goalName.isEmpty()).toBe(false);
        expect(goalDescription.isEmpty()).toBe(false);

        goalName.simulate('change', { target: { value: 'My Goal' }});
        goalDescription.simulate('change', { target: { value: 'A goal description' }});

        // Next page

        wrapper.find('#next').simulate('click');
        expect(wrapper.find(GoalDetails).isEmpty()).toBe(true);
        expect(wrapper.find('#prev').isEmpty()).toBe(false);
        expect(wrapper.find('#next').isEmpty()).toBe(true);
        expect(wrapper.find('#submit').isEmpty()).toBe(false);

        // Page 2 - Step Details

        const stepDetails = wrapper.find(StepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        const stepName = stepDetails.find('input[name="stepName"]');
        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepName.isEmpty()).toBe(false);
        expect(stepDescription.isEmpty()).toBe(false);


        stepName.simulate('change', { target: { value: 'My Step' }});
        stepDescription.simulate('change', { target: { value: 'A step description' }});

        expect(wrapper.find('input[name="goal_name"]').prop('value')).toBe('My Goal');
        expect(wrapper.find('input[name="goal_description"]').prop('value')).toBe('A goal description');
        expect(wrapper.find('input[name="step_name"]').prop('value')).toBe('My Step');
        expect(wrapper.find('input[name="step_description"]').prop('value')).toBe('A step description');
    });
});
