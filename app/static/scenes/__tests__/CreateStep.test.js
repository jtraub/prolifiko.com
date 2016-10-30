import React from 'react';
import CreateStep from '../CreateStep';
import Scene from '../../components/Scene';
import { CustomStepDetails } from '../../components/StepDetails';
import StepDeadline from '../../components/StepDeadline';
import Textarea from '../../components/Textarea';
import moment from 'moment';
import {mount} from 'enzyme';

describe('<CreateStep/>', () => {
    it('renders a scene to create a step with custom deadline', () => {

        const wrapper = mount(<CreateStep csrfToken="foo" stepNumber={1} />);
        const scene = wrapper.find(Scene);

        // there should be 1 page
        expect(scene.props().pages.length).toBe(2);

        const stepDetails = scene.find(CustomStepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        // find the name and desc elements and verify they're empty
        const stepName = stepDetails.find('textarea[name="stepName"]');
        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepName.isEmpty()).toBe(false);
        expect(stepDescription.isEmpty()).toBe(false);

        // there shouldn't be 'prev' and 'submit' buttons on first page
        expect(wrapper.find('#previous').isEmpty()).toBe(true);
        expect(wrapper.find('#submit').isEmpty()).toBe(true);

        // ensure submit button is disabled
        const next = wrapper.find('#next');
        expect(next.prop('disabled')).toBe(true);

        // populate form with valid data
        stepName.simulate('change', { target: { value: 'My Step' }});
        stepDescription.simulate('change', { target: { value: 'A step description' }});

        // verify the button is now enabled and simulate click
        expect(next.prop('disabled')).toBe(false);
        next.simulate('click');

        expect(wrapper.find('#next').isEmpty()).toBe(true);
        expect(wrapper.find('#prev').isEmpty()).toBe(false);

        const submit = wrapper.find('#submit');
        expect(submit.isEmpty()).toBe(false);
        expect(submit.prop('disabled')).toBe(true);

        const stepDeadline = scene.find(StepDeadline);
        expect(stepDeadline.isEmpty()).toBe(false);

        wrapper.find('.suggestion--1').simulate('click');

        expect(wrapper.find('input[name="step_name"]').prop('value')).toBe('My Step');
        expect(wrapper.find('input[name="step_description"]').prop('value')).toBe('A step description');
        const expectedDeadline = moment().add(1, 'day').format('YYYY-MM-DD');
        expect(wrapper.find('input[name="step_deadline"]').prop('value')).toBe(expectedDeadline);
    });

});
