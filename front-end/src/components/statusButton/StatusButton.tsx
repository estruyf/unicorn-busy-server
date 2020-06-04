import * as React from 'react';

export interface IStatusButtonProps {
  apiUrl: string;
  className: string;
  text: string;
  callApi: (url: string) => Promise<void>;
}

export const StatusButton: React.FunctionComponent<IStatusButtonProps> = (props: IStatusButtonProps) => {
  return (
    <button className={`btn btn-lg btn-block ${props.className}`} onClick={() => props.callApi(props.apiUrl)}><b>{props.text}</b></button>
  );
};