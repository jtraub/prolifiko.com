import React from 'react';
import CreateMidnightStep from '../CreateMidnightStep';
import Scene from '../../components/Scene';
import StepDetails from '../../components/StepDetails';
import Textarea from '../../components/Textarea';
import {mount} from 'enzyme';

describe('<CreateMidnightStep/>', () => {

    it('renders a scene with one page', () => {

        const wrapper = mount(<CreateMidnightStep csrfToken="foo" stepNumber={1} />);
        const scene = wrapper.find(Scene);

        // there should be 1 page
        expect(scene.props().pages.length).toBe(1);

        const stepDetails = scene.find(StepDetails);
        expect(stepDetails.isEmpty()).toBe(false);

        // find the name and desc elements and verify they're empty
        const stepName = stepDetails.find('input[name="stepName"]');
        const stepDescription = stepDetails.find(Textarea).find('textarea');

        expect(stepName.isEmpty()).toBe(false);
        expect(stepDescription.isEmpty()).toBe(false);

        // there shouldn't be 'prev' and 'next' buttons because there is only one page
        expect(wrapper.find('#prev').isEmpty()).toBe(true);
        expect(wrapper.find('#next').isEmpty()).toBe(true);

        // ensure submit button is disabled
        const submit = wrapper.find('#submit');
        expect(submit.prop('disabled')).toBe(true);

        // populate form with valid data
        stepName.simulate('change', { target: { value: 'My Step' }});
        stepDescription.simulate('change', { target: { value: 'A step description' }});

        // verify the button is now enabled
        expect(submit.prop('disabled')).toBe(false);
    });

});
