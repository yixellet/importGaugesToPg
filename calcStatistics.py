def calcMeanAnnuals(conn, cursor, schemaName, gauges):
    """
    Вычисляет среднемноголетние отметки (за безледный и за весь период)
    """
    
    cursor.execute(
        """
        CREATE MATERIALIZED VIEW IF NOT EXISTS {0}."meanAnnualsCalc"
        AS
        SELECT gauges.uuid,
                gauges."calcMeanAnnualTotal"(gauges.code) AS "allPeriod",
                gauges."calcMeanAnnualIceFree"(gauges.code) AS "iceFree"
        FROM {0}.gauges
        WITH DATA;

        ALTER TABLE IF EXISTS {0}."meanAnnualsCalc"
            OWNER TO postgres;
		""".format(schemaName)
	)
    conn.commit()

    """
    SELECT date_part('year', date) AS year,
			avg(stage) AS meanStage,
			min(date) AS startDate,
			max(date) AS endDate
	FROM hydro."77808abs"
	WHERE date_part('month', date) < 7 AND (
		'b65abc16-ece4-4ed9-91c9-222d2c953c37' = ANY(props) OR
		'8ea93aac-184a-43be-a5da-3bb7772b5813' = ANY(props) OR
		'35f4cf59-0c0e-4aba-a0de-264b157b5d72' = ANY(props) OR
		'4cbbb549-f9a7-4864-8ddd-61e19c60d0fc' = ANY(props) OR
		'7e43f9d2-9277-4561-8693-957b47978865' = ANY(props) OR
		'cd1dd311-1d9e-41d6-8ac5-8e2c8ca33791' = ANY(props) OR
		'24696dda-f014-47c5-9b27-e99ef4c3ff95' = ANY(props) OR
		'e341c76a-0254-430a-8ec0-7251a5f4905f' = ANY(props) OR
		'a5290a31-7678-4dcd-88df-808731e2ea39' = ANY(props) OR
		'e5724a18-9b5a-41b1-af2e-f27df4a9ec3c' = ANY(props) OR
		'9a5877ce-cb37-4fee-a7f1-ff99121ece1e' = ANY(props) OR
		'97669f6c-eb3d-4f31-8bd4-df24ba34b82f' = ANY(props) OR
		'7331493a-6816-4cab-b656-834711a6df28' = ANY(props) OR
		'55721775-7290-423f-b2c6-69e6d11ff081' = ANY(props) OR
		'1aca6253-9524-4682-9530-676c19bed571' = ANY(props) OR
		'b7f6371e-95af-4f00-bd8e-e101881abce3' = ANY(props) OR
		'79b84077-6822-4c57-9d8f-e62995783d93' = ANY(props) OR
		'8e79857f-212b-44a7-9916-c9080b5a72d2' = ANY(props) OR
		'8a03655f-f288-4b46-8cd6-0c1cb711d946' = ANY(props) OR
		'5ce4ecbb-24e7-4c5e-90af-2102e0f08528' = ANY(props) OR
		'c041ec57-32e2-46da-94ab-1f23479f9cd5' = ANY(props) OR
		'04cf215b-2f47-4931-990a-a6d147c3ed59' = ANY(props) OR
		'ff9bd678-6d16-4328-ae91-e027d5f33456' = ANY(props) OR
		'10cb947c-8e32-4c4b-bca0-0588c33f3811' = ANY(props) OR
		'321167b5-8104-43fe-a178-c260321fa779' = ANY(props) OR
		'b240ae01-ea5e-48c0-a0df-db6082dcce9d' = ANY(props) OR
		'dc7142cc-6f30-4d72-9dc3-a211e08a2ed7' = ANY(props) OR
		'0f0e7829-a741-4398-84d6-2d62886242aa' = ANY(props) OR
		'2624dbc7-062e-4fa6-8445-b413b9e997a7' = ANY(props) OR
		'0b54894c-e126-4a24-9eec-a5c02f6da610' = ANY(props) OR
		'cfde22da-a8e9-44d7-bf2d-986da12ebc52' = ANY(props) OR
		'da95b2ac-6b65-4d3e-b797-40eb75dd4f64' = ANY(props) OR
		'7341edf0-3c29-4ec8-8961-e7dbff40ab15' = ANY(props) OR
		'12682edb-1b2c-4b64-82ad-037ed75f6fb7' = ANY(props) OR
		'4e71f205-312e-4641-8b4b-189ce6dbb569' = ANY(props) OR
		'3b5b3ce1-b7f3-4ab4-8cb7-92f74b2e8127' = ANY(props))
	GROUP BY year"""