import * as React from 'react';
import { RGB } from '../../models';

export interface IStatusProps {
  status: string | null;
  rgb: RGB | null;
}

export const Status: React.FunctionComponent<IStatusProps> = (props: IStatusProps) => {
		
	return (
		<>
      <h2 className="font-weight-light text-center">
        {props.status ? (
          <>
            <span>Current status: </span>
            <span className="badge badge-pill badge-primary" style={{
              backgroundColor: props.rgb ? `rgb(${props.rgb.red}, ${props.rgb.green}, ${props.rgb.blue})` : 'inherit'
            }}>{props.status}</span>
          </>
        ) : `Busy Light`}  
      </h2>
    </>
	);
};