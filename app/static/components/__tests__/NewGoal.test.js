import React from 'react';
import NewGoal, {SetGoal, FirstStep, Timezone} from '../NewGoal';
import Textarea from '../Textarea';
import {mount} from 'enzyme';

require('debug').enable('*');

describe('<NewGoal/>', () => {
  let wrapper;

  it('works', () => {
    wrapper = mount(<NewGoal csrfToken="foo"/>);

    const setGoal = wrapper.find(SetGoal);
    const textArea = setGoal.find(Textarea).find('textarea');

    expect(setGoal).not.toBeNull();
    expect(textArea).not.toBeNull();

    // input goal data and submit
    textArea.simulate('change', { target: { value: 'My Goal'}});
    setGoal.find('button').simulate('click');

    // assert form updates and `next` loads
    expect(wrapper.find('input[name="text"]').prop('value')).toBe('My Goal');
    expect(wrapper.find(FirstStep)).not.toBeNull();

    // input step data and submit


    // assert form updates and `next` loads


    // expect(wrapper.instance().state.text).toEqual('My Goal');
    //
    // expect(wrapper.contains(GoalName)).toBe(false);
    // expect(wrapper.contains(GoalDescription)).toBe(true);



  });
});