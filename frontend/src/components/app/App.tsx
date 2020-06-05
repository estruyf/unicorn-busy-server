import React from 'react';
import './App.css';
import { Status } from '../status';
import { RGB, StatusInfo } from '../../models';
import { StatusButton } from '../statusButton';

export function App() {
  let timer: number | null = null;
  const [status, setStatus] = React.useState<string | null>(null);
	const [rgb, setRgb] = React.useState<RGB | null>(null);
	const [overwritten, setStatusOverwritten] = React.useState<boolean>(false);

  const fetchStatus = async () => {
    const data = await fetch(`/api/status`);

    if (data && data.ok) {
      const statusInfo: StatusInfo = await data.json();
      if (statusInfo && statusInfo.status) {
        setStatus(statusInfo.status);
        setRgb({
          red: statusInfo.red,
          green: statusInfo.green,
          blue: statusInfo.blue,
        });
        setStatusOverwritten(!!statusInfo.statusOverwritten);
      } else {
        setStatus(null);
        setRgb(null);
      }
    }

    timer = window.setTimeout(() => {
      fetchStatus();
    }, (1 * 60 * 1000));
  }

	React.useEffect(() => {
    fetchStatus();
  }, []);

  const callApi = async (url: string) => {
    if (url) {
      const data = await fetch(url, { method: "POST", body: JSON.stringify({}) });
      if (data && data.ok) {
        if (timer) {
          clearTimeout(timer);
        }
        fetchStatus();
      }
    }
  };
  
  return (
    <div className="app container py-4">
      <section className="row">
			  <div className="col">
			    <Status status={status} rgb={rgb} />
        </div>
      </section>

      <section className="row mt-4">
			  <div className="col-sm-12 col-md-6 col-lg-3 mb-4">
			    <StatusButton apiUrl={"/api/available"} className={"btn-success"} text={"Available"} callApi={callApi} />
        </div>
        <div className="col-sm-12 col-md-6 col-lg-3 mb-4">
			    <StatusButton apiUrl={"/api/busy"} className={"btn-danger"} text={"Busy"} callApi={callApi} />
        </div>
        <div className="col-sm-12 col-md-6 col-lg-3 mb-4">
			    <StatusButton apiUrl={"/api/away"} className={"btn-warning"} text={"Away"} callApi={callApi} />
        </div>
        <div className="col-sm-12 col-md-6 col-lg-3 mb-4">
			    <StatusButton apiUrl={"/api/rainbow"} className={"btn-secondary rainbow"} text={"Rainbow"} callApi={callApi} />
        </div>
      </section>

      <section className="row">
			  <div className="col-sm-12 col-md-6 mb-4">
          <StatusButton apiUrl={"/api/on"} className={"btn-outline-success"} text={"On"} callApi={callApi} />
        </div>
        <div className="col-sm-12 col-md-6 mb-4">
          <StatusButton apiUrl={"/api/off"} className={"btn-outline-dark"} text={"Off"} callApi={callApi} />
        </div>
      </section>

      {
        overwritten && (
          <section className="row mt-4">
            <div className="col">
              <StatusButton apiUrl={"/api/reset"} className={"btn-outline-danger"} text={"Reset"} callApi={callApi} />
            </div>
          </section>
        )
      }
		</div>
  );
}
