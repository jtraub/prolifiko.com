import React from 'react';
import CreateGoal, { GoalTarget } from '../CreateGoal';
import Textarea from '../Textarea';
import { mount } from 'enzyme';
import moment from 'moment';

it('<CreateGoal/>', () => {
    const wrapper = mount(<CreateGoal csrfToken="foo"/>);

    const goalTarget = wrapper.find(GoalTarget);

    expect(goalTarget).not.toBeNull();

    goalTarget.find('[aria-label="day-1"]').first().simulate('click');
    goalTarget.find('button').simulate('click');


    expect(wrapper.find('input[name="goal_target"]').prop('value')).toEqual(moment().date(1).format('YYYY-MM-DD'));


    //const textArea = setGoal.find(Textarea).find('textarea');

    //expect(setGoal).not.toBeNull();
    //expect(textArea).not.toBeNull();

    // input goal data and submit
    //textArea.simulate('change', { target: { value: 'My Goal'}});
    //setGoal.find('button').simulate('click');

    // assert form updates and `next` loads
    //expect(wrapper.find('input[name="text"]').prop('value')).toBe('My Goal');
    //expect(wrapper.find(FirstStep)).not.toBeNull();

});