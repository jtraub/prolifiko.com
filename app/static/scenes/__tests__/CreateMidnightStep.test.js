import React from 'react';
import CreateMidnightStep from '../CreateMidnightStep';
import Scene from '../../components/Scene';
import { MidnightStepDetails } from '../../components/StepDetails';
import Textarea from '../../components/Textarea';
import {mount} from 'enzyme';

describe('<CreateMidnightStep/>', () => {
    it('renders a scene with one page', () => {
        const wrapper = mount(<CreateMidnightStep csrfToken="foo" stepNumber={1} />);
        const scene = wrapper.find(Scene);

        // there should be 1 page
        expect(scene.props().pages.length).toBe(1);

        const stepDetails = scene.find(MidnightStepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepDescription.isEmpty()).toBe(false);

        // there shouldn't be 'prev' and 'next' buttons because there is only one page
        expect(wrapper.find('#prev').isEmpty()).toBe(true);
        expect(wrapper.find('#next').isEmpty()).toBe(true);

        // ensure submit button is disabled
        const submit = wrapper.find('#submit');
        expect(submit.prop('disabled')).toBe(true);

        // populate form with valid data
        stepDescription.simulate('change', { target: { value: 'A step description' }});

        // verify the button is now enabled
        expect(submit.prop('disabled')).toBe(false);

        expect(wrapper.find('input[name="step_name"]').prop('value')).toBe('First Step');
        expect(wrapper.find('input[name="step_description"]').prop('value')).toBe('A step description');
    });

});
