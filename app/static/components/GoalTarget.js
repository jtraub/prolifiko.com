import React from 'react';
import moment from 'moment';
import DatePicker  from 'react-datepicker';

export default class GoalTarget extends React.Component {
    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
    };

    onChange(date) {
        this.props.onChange({goalTarget: date.format('YYYY-MM-DD')}, true);
    }

    render() {
        let selected;

        if (this.props.data) {
            selected = moment(this.props.data.goalTarget);
        }

        return (
            <div>
                <section>
                    <p>Your first task to decide when you'd like to achieve this goal by.</p>

                    <p>We suggest you target 5-10 days.</p>
                </section>

                <DatePicker inline selected={selected} onChange={this.onChange.bind(this)}/>
            </div>
        );
    }
}
