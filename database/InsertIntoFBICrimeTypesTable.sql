INSERT INTO FBICrimeTypes (FBIType, Description, Against, Severity)
SELECT dft.`FBI Type`, dft.Description, da.Against, ds.severity
FROM DictFBIType dft
JOIN DictAgainst da ON dft.`FBI Type` = da.`FBI Type`
JOIN DictSeverity ds ON dft.`FBI Type` = ds.`FBI Type`