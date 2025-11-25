Run locally:

1. azd env new
2. Deploy BLUE
    ```
    azd env set BLUE_COMMIT_ID fb699ef
    azd env set LATEST_COMMIT_ID fb699ef
    ```
3. Run `azd up`
   
4. Deploy Green, but keeping traffic on BLUE 
    ```
    azd env set GREEN_COMMIT_ID c6f1515
    azd env set LATEST_COMMIT_ID c6f1515
    azd env set PRODUCTION_LABEL blue

    azd deploy
    ```

    To test
    ```powershell
    $uri = azd env get-value | Select-String "SERVICE_WEB_URI"; $domain = ([System.Uri]$uri).Host.Split('.', 2)[1]; Write-Host "Production FQDN: $uri"; Write-Host "Blue label FQDN: https://web---blue.$domain"; Write-Host "Green label FQDN: https://web---green.$domain"
    ```
    
    See traffic:
    ```
    az containerapp ingress traffic show --name web --resource-group <your-resource-group> -o table
    ```

5. Send production traffic to the green revision

    ```
     azd env set PRODUCTION_LABEL green
     azd deploy
    ```

6. Roll back     
    
    ```
    azd env set PRODUCTION_LABEL blue
    azd deploy
    ```
