import React from 'react';
import CreateFiveDayChallenge from '../CreateFiveDayChallenge';
import CreateStep from '../StepDetails';
import CreateGoal from '../GoalDetails';
import Textarea from '../Textarea';
import {mount} from 'enzyme';

describe('<CreateFiveDayChallenge/>', () => {
  let wrapper;

  it('works', () => {
    wrapper = mount(<CreateFiveDayChallenge csrfToken="foo"/>);

    const setGoal = wrapper.find(CreateGoal);
    let textArea = setGoal.find(Textarea).find('textarea');

    expect(setGoal).not.toBeNull();
    expect(textArea).not.toBeNull();

    // input goal data and submit
    textArea.simulate('change', { target: { value: 'My Goal'}});
    setGoal.find('#next').simulate('click');

    // assert form updates and `next` loads
    expect(wrapper.find('input[name="text"]').prop('value')).toBe('My Goal');

    const createStep = wrapper.find(CreateStep);
    textArea = createStep.find(Textarea).find('textarea');

    expect(createStep).not.toBeNull();
    expect(textArea).not.toBeNull();

    // input step data and submit
    textArea.simulate('change', { target: {value: 'Step 1'}});
    createStep.find('#submit').simulate('click');

    // assert form updates and `submit` loads
    expect(wrapper.find('input[name="first_step"]').prop('value')).toBe('Step 1');
  });
});
