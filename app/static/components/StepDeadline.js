import React from 'react';
import moment from 'moment';
import DatePicker from 'react-datepicker';

export default class StepDeadline extends React.Component {

    static propTypes = {
        onChange: React.PropTypes.func.isRequired,
        data: React.PropTypes.object.isRequired,
    };

    static defaultProps = {
        data: {
            stepDeadline: moment().add(1, 'days').format('YYYY-MM-DD'),
        }
    };

    onChange(date) {
        this.props.onChange({ stepDeadline: date.format('YYYY-MM-DD') }, true);
    }

    render() {

        const selected = moment(this.props.data.stepDeadline);

        return (
            <div>
                <section>
                    <p>Choose a deadline for this step</p>

                    <p>We suggest you target 24-48 hours.</p>
                </section>

                <DatePicker inline minDate={moment().add(1, 'days')} selected={selected} onChange={this.onChange.bind(this)}/>
            </div>
        );
    }
}
