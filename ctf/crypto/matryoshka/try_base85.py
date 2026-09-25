import base64

body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)

for name, s in [("normal", body), ("reversed", body[::-1])]:
    for fn_name, fn in [("a85", base64.a85decode), ("b85", base64.b85decode)]:
        try:
            r = fn(s.encode())
            print(name, fn_name, "OK:", r)
        except Exception as e:
            print(name, fn_name, "FAIL:", e)
