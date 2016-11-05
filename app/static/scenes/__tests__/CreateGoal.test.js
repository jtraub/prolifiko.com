import React from 'react';
import CreateGoal from '../CreateGoal';
import GoalTarget from '../../components/GoalTarget';
import { CustomGoalDetails } from '../../components/GoalDetails';
import { CustomStepDetails } from '../../components/StepDetails';
import StepDeadline from '../../components/StepDeadline';
import Textarea from '../../components/Textarea';
import { mount } from 'enzyme';
import moment from 'moment';

describe('<CreateGoal/>', () => {
    let wrapper;

    it('prompts for goal and step details', () => {
        wrapper = mount(<CreateGoal csrfToken="foo"/>);

        // Page 1 - CustomGoalDetails

        const goalDetails = wrapper.find(CustomGoalDetails);
        expect(goalDetails.isEmpty()).toBe(false);

        const goalName = goalDetails.find('textarea[name="goalName"]');
        const goalDescription = goalDetails.find(Textarea).find('textarea');

        expect(goalName.isEmpty()).toBe(false);
        expect(goalDescription.isEmpty()).toBe(false);

        goalName.simulate('change', { target: { value: 'My Goal' }});
        goalDescription.simulate('change', { target: { value: 'A goal description' }});

        // Next page

        wrapper.find('.next').simulate('click');
        expect(wrapper.find('.prev').isEmpty()).toBe(false);
        expect(wrapper.find('.next').isEmpty()).toBe(false);
        expect(wrapper.find('.submit').isEmpty()).toBe(true);

        // Page 2 - GoalTarget

        const goalTarget = wrapper.find(GoalTarget);
        expect(goalTarget.isEmpty()).toBe(false);

        wrapper.find('.suggestion--1').simulate('click');

        // Next page

        wrapper.find('.next').simulate('click');
        expect(wrapper.find(CustomGoalDetails).isEmpty()).toBe(true);
        expect(wrapper.find('.prev').isEmpty()).toBe(false);
        expect(wrapper.find('.next').isEmpty()).toBe(false);
        expect(wrapper.find('.submit').isEmpty()).toBe(true);

        // Page 3 - Step Details

        const stepDetails = wrapper.find(CustomStepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        const stepName = stepDetails.find('textarea[name="stepName"]');
        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepName.isEmpty()).toBe(false);
        expect(stepDescription.isEmpty()).toBe(false);

        stepName.simulate('change', { target: { value: 'My Step' }});
        stepDescription.simulate('change', { target: { value: 'A step description' }});

        // Next page

        wrapper.find('.next').simulate('click');
        expect(wrapper.find(CustomStepDetails).isEmpty()).toBe(true);
        expect(wrapper.find('.prev').isEmpty()).toBe(false);
        expect(wrapper.find('.next').isEmpty()).toBe(true);
        expect(wrapper.find('.submit').isEmpty()).toBe(false);

        // Page 4 - Step Deadline

        const stepDeadline = wrapper.find(StepDeadline);
        expect(stepDeadline.isEmpty()).toBe(false);

        wrapper.find('.suggestion--1').simulate('click');

        const expectedTarget = moment().add(7, 'days').format('YYYY-MM-DD');
        expect(wrapper.find('input[name="goal_target"]').prop('value')).toBe(expectedTarget);
        expect(wrapper.find('input[name="goal_name"]').prop('value')).toBe('My Goal');
        expect(wrapper.find('input[name="goal_description"]').prop('value')).toBe('A goal description');
        expect(wrapper.find('input[name="step_name"]').prop('value')).toBe('My Step');
        expect(wrapper.find('input[name="step_description"]').prop('value')).toBe('A step description');
        const expectedDeadline = moment().add(1, 'days').format('YYYY-MM-DD');
        expect(wrapper.find('input[name="step_deadline"]').prop('value')).toBe(expectedDeadline);
    });
});
