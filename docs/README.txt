FiBridge - Important Usage Instructions
======================================

Before you start using FiBridge, you MUST generate SSL certificates for HTTPS support.

Step 1: Generate SSL Certificates
---------------------------------
Open a command prompt in the root directory of FiBridge and run:

    cd _internal
    scripts\generate_cert.bat

Then, the command line prompts you to enter information such as country, email, etc. Follow the instructions to fill in the required details; you can press Enter to accept the default value or leave a field blank. After completing all prompts, you will see the following prompt indicating success:

    Certificates generated: key.pem, cert.pem
    Press any key to continue ...

This will create the required certificate files for secure HTTPS communication in the following folder:

_internal\cert.pem
_internal\key.pem

It is suggested to navigate to the folder "_internal\configs" to confirm the existence of these two files.

Step 2: Start FiBridge
----------------------
After certificates are generated, you can run the main program (FiBridge_v1.0.0_x64_win.exe) in the root folder.

Since using self-signed SSL certificates, your browser may prompt that the connection is in risk. Feel free to "ignore" or "proceed anyway" after selecting "advanced options". No actualy risk is involved if you generated the certificate by your own and if you run the app locally.

If you do not generate certificates first, HTTPS features (such as remote scan) will NOT work.

For any questions or issues, please refer to the project documentation or contact the author.
