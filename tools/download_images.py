"""
Download the photos and figures from the old Google Sites homepage
(www.picogigalab.com) into assets/img/.

KIST's network blocks googleusercontent.com, so run this from another
network (home Wi-Fi, a phone hotspot, etc.):

    python tools/download_images.py

Files that already exist are skipped. Re-run with --force to overwrite.
"""
import os
import sys
import urllib.request

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
WIDTH = 1600  # Google resizes on the fly; this is the longest edge requested

IMAGES = [
    ("misc/contact.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uWbUHh_o-guaehJxv4bAVWvb-aOalfBJfNDASmyKpT5WW98nPBGcWEKJSKSYUun1ciZVd7d9Hgq3iejkX4ToRnSZMC8sJXkA7Oi4xX_TxjzS9uES3vHMD3fTdXvYkOezt7kTcCOe9SOJmFMen0URF-ldY9LINh6OdisiCQcHWktv9oq9Q2_oQe3MOhb2IYEgEhXDtjcMI8vIhbfiNs--Jt78WuDpWzzAO6SKNZ"),
    ("misc/home-hero.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tIh5ccgyC8BgtsogSKXiacH6T3mmZdOS-OvZDoXoSQ5FlnjWy48PeB_u0Gy1NWptAwHf9JCCV3BRz7bTXo2fYS-54VartKYdk8G3MlqHu0CuUXRR-ZapHXSv_9beKcFWlY5LQ81DCPvISd90O6Tt1ay0GWYCPL_QVgfTf1CU6UswJFvxyr7JtKjUb5NPAHNSWqdnCL04MHencR_c9tNApKC3vLfc-nGyj08F_1Zz0"),
    ("news/n02.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vS7L82HX7NiY55tXW9WWQGRnZgRTLbVoXD3NRaQXLbkeuGBqeVkKeoObCpStGq7Od9woLJ-m18QftOR4H68Ts_AMTrP3pXiuTJM-Eq7w8xOfCv89t-DUxcfT1kfNEZxclZ3P99kTxHlxH1Gm0kxbyyOChfV1ls9M-LHFlDamKITdPimMHxlPI1gdEyXKDbgQNpzCc3Lng2puGHMg2DxBpzFJag8uP7PNVdsEypwfg"),
    ("news/n03.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uLzO-Yuw4z6ka3-3vnxGA9czAr0z4Ec1AWNPAzznHBZLXB0s3a6SjsOid-uFp4RhkUYjuuupPC_VodfS1gWZ3IQX8ngHAkByRv4UrHmviRQ546Cm-SSeoqMsAyeI6cAhL5FQPWe6eJ5sgr9MXNRcDdTvuxnP0ccxSJuyeDxFoaFx5J-YGKOm4gCyc4-SkylqDe2GAIydWev2zDma3xapz7L5nF_Nj4w8RYxM6dRnw"),
    ("news/n04.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72u5VMEZ6Tvj_DSqfG9QI0ftNFa1o_AbVH5TkElUvQKq2WzTqTryvQRINAAtlIWTMTBdI2P98ctotDkAc6ebSb_VM3jPZ7SPe5UqcNPKZzDBqPuO057u4kSCuR6KBpSa529sILpiRoX_OJ_wpBwtGXF99VUYYGVZ2d100uEeqFag6NVSRvulNGMw8F7HTtC29ge11Vl-NUp6oca2SIRzKA53zDx3Sya8FC6yClX_uQg"),
    ("news/n05.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sOuq7o0t2OSvdi7d6JTl1mfEM0dkeE217DDHjf4HnOvLIKrLNBhXdkFxH9S-YkRjDkmyCx1nyraQflXn-Ae24OjArLGxNxT3-jbSvzYhB8LCzVXhSARlN9fK9I-i9TuoYzWnMd2LNMnuTMxKrRBdWvm5x1r3XsLoVXD7Pb7R0C-k9GiVi81vTWAjlXm4ybZiscKKGQixhMtahENZAtGbBOdxhmwq_g0GJB5Z-ev3A"),
    ("news/n06.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sh-RRwQtJAF5fwLbKGztrvJ5Fpb-tM_EdZE5_rbb0xdKehC9pQlXWnGEhfVgFLghL9X7PP1ttnYcRrOzOmvBEt745E9S9ep-iRnHjyNBjzr8FA_HhsPaN8AaLAjZMSBdikzNB_u3ywnYx4cdcX8kytFjfzTOfpowIRVC_p6XVyGUBjcvUJPbFaQ9kA-ELMQzG1-lZct6a2pBUR2vXlQ6T47CHoHkSgzwUb3SE-GC8"),
    ("news/n07.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vugrccwo5YJylfq0xxCjXZbTH95FDszlgsw-1rBJ28Wata796cBJDuCSfTuEGImrkXDNbWH1_NN4HopfK0diwkvcMkjdLXPgOv-QNL5lYPZ2FuX6-AK16CUAJ5zAcjpoXCeUCyy-0JayoXeq1i7dykx7h44OLCm5oXtocRg2jHF8Eep_s22ewMQqxLj9GpnZ9edVfJIahSnv5CF6ON1zwCo9nB8VRpkAGVSJnoTEM"),
    ("news/n08.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72v8WhVQUYHDhXSdJckP0CenYAX_gnSh-kkCGEb7i3ztJJXZTNgWaH2fHhfOOMl4aKRpSNnaCiULI5qTx4RxYlVH0IP2YuP5lHWjA1LOmXTJJ3acZk807_m-wCLf5LATt2T_vnP9N8CLQrmP3oPnV24v0-yFKRFle1lDKVp4f1u6_P4JJoL9dzAEkmEgpjMK7NmFDrTFti2HjKIB83lKfrsMos26Wz2qt_BAGv2H"),
    ("news/n09.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72u2YqqmJS3NbYsNh3WlE_gLvG3YIsznBzG74uKJl_CC288l3ML3L8PZU-P1vLVOm_mADughfRZ7sElsq0FKIC0VmrFKd78jZfjZDXWRViEmH3BR724n1MWMFdRCE-Veqh5jO8pIYNrP_Mz4p-8hxKHopy0pESn7GIntlfqShPHWEAi4pBIvPLkE3VMeobc"),
    ("news/n10.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vSEMvUBd55cAe3QfJddLogSj7ILlAcGp2leSm6fks9J1d2Wa5zmQzbBtvXxZ0N5FU1AbpNssjyfdAfOv84x2Xx9C1AGKpdfts3tDBKXWHeW9bnTp4BLwRlwd1HFXxifnwgpX0k6kcH19Xnw9FKfEFtDDtXbjJs6YrTQjjz19ExQ861vX1fBa5pIRrA"),
    ("news/n11.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sxUqo-b8Z1dA1KBUiL4zLYRKXd6VGS5stwGTB4YiA2XL6FqAPiVK_wAb_GTnaCfRfqu55zAY5O0iUoHi1f12FOPlAlUPZbaSVQ6LRUup_Ini07X1l3c7t_MJWT0Fpf1bzSi0IA4o6HAQ9mb3iKU4JtyApSCtsjVeScXnrvqnthCpD-X1YOw2e9TiGwK4K5PXCnZpBNozNRlwQ3pOFSlhoCDCwOfomIszhVLCwQKYM"),
    ("news/n12.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72ubBbY7VHlaNlNTWYFw1aNK2Wa8Dkm67_emNBBBjgqhEgj1jzA_OdfMmO1Kw6EkqBzEFp_DwGeq3AqnXlviutTyTfxS5Mq4wy5MPDZROTAPW3n0TVFVLn0_jZfWfX8sMIt8s99pj8BbSb3f4HAQQjFlkW1oMwv1S6faEJ-H1SQ0PZk1eUD8hoA-9nGd8lE"),
    ("news/n13.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72s3LoAdoGM9gSF8y_2lta55I8FLmpx4NI68KXS6KgPGwXYcArSWYOeMiDVgIvkvJuTZ8iUQX4tbZ0qDZTp6ke0AQLG09On93TehZHttAUhMSbjTC2wu-Rx0y1ETN4_tYFhMruwnFCCb4ZuJ3L7f9M4wMcUn1WrWqh5F1EmeH3ooG8WA94vKTWUnNzKRDTRQ-4laDlnHkk65eAzV7etsfCmWdpyYZ9NjQXU0VvKXXmA"),
    ("news/n14.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vSFScXcM8qtalHsF9LTuga1bo9otuSXmYo1V-GjdYu3dgnCl4WzSqKvAM0cWoLosTDAoYE0H-cifdRB0xyU8oqmozpZxO-TQYb68m5OpZ47ycaVQ8ZS_gXtJYxMGKOk8FTTkDDAiKiYW55vCGYK98Cadvl-xmX7WCb2-BOmKwazAAknCL_thP1us2H6Uk"),
    ("news/n15.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uC4QMbCJLAaVU71dfhunRjRnVpQnbc9gCEJqjeh8irZui2kwqyo1z6Y2OyCIl_dih6sMtFC4qwrqqu91z3srXfH1bx3s2o-LkIBCz29LdAAmJWeOMJR6BwK5QQEg09xZD1oJs3DCHGBgBzgbqxlkDc6G4C3XfRMP8-PtZKovdAeJI5ZSOTSc20Q4LKFOAF_VBXzfCdeY1eyJ-ajp5oA4RAiTeBfUir16-NrIfU"),
    ("news/n16.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sVn1UAuis5-KzHmuwkiE1H1FnMDahhLqYnrg4tWfcU27RY5ybNB_e8BfxmuH6zZwBSQrmfHzGJndR60CDvCgGAiQcDg2MMeP13uDlQqcOI_MZkBEe2946yOQt_Ni8X8gAdoPXJE73-gRdIdDO0of0yL4AySfIFJ7CH5N6awhq-Xpyhnkt3BaqJf-HQz4t5zEZvzXpCmvvem0BnjdAuI_X5GEDK991GUXJehUqG"),
    ("news/n17.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tHC66ZjyjA40YxuS2PyWZg6IjTRv7lIGMRbkrWXp715vjAJwXzyrfrYlrH6_CGmJr6Q3ymZvfZ_WTXGx_WvSz4Lvojr7aHjzhhZ8sleWbYcniVoC0JKl3Lhp5BfwJE7wkXFfM8MjMU2TwX1VvatkBqBFMkAd-Ore0OOPy1hpQzk9LGCElbqlEKZd-BdINwGl9jQOqPnxr3fZlg8eYMxX2btS-SGfNa3cBtiquj9fA"),
    ("news/n18.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72ttIkIs2z1zp5WuYjcSJmqVpaXx3_hC2ILhqD839U-SOFvICIO_Qz8X_dAPfalC-ny0aUJmC-oa40-7W4Z2TI-JKR53Bnz3cFdx1DB-YG-ph4rb2xwYnl9kOxNov53oyTk4dX7lIcDrTItORRziOMi4RiijmRzEWivg1A0eGejjY54PcvRj9Fc6hVQdYVsJz-UxwVRKQwySkpDVzJTefINHijv9xfBoWJM-cvVh86Y"),
    ("news/n19.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vTCuiASj29Qwkj47G_vcTIlZi1cSoxx3KWQal7M7Q1qWzmo4V-SHfe3nENV6xepf1tAijlYn8JljaOGgpihSG_6sJUr81CUHnPNMinxHa-iIRWi4Slm829xWN8ZsHZ8YnXxiphhU3DpkcPopoOew18AQENLSTp4E5S9qxIj6Y4j82xc3BSf7UIAJ0jFdb3Ja7Gf3TWqOfS2rG5CSJ69AYMwlbV5Hkptx2O2Ic5"),
    ("news/n20.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tXZ9kslD44tWGMwCZxJzoBerud5Wc1TPL4v6Z18Mvnn7zFhCJKyhLCqxHXmXSZOufGTLO4rmoVfwRUUjsJkMXaJD-_PEBph-Ut-xiKqpMNI7K0nd8inaua8UdOsMJssvtO7IqUD-q-yYdrzHKWDD5V7R0a1K6z4dMy3As07b5i9H0JtE3G13yE0i2keNwjmGIeI76tbuyJz2RQSAwXMZ8nlWV77UyN1ExcStsY3Oc"),
    ("news/n21.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tj5KeWaAC_Sr7UF4chIYfdGaB9x7u9gkYXZJdBGFA4P9PuWlqTPnDmK8oQ5OALXDiFaFI2z_SeXgh7GF7y4fBYqDYO9WobYIhdaisTsOfPRlt28fVrkKSDb1Cq09aXU3C7qjGJxpn-vY1meSRWc07WMSVdmnmE4Fna0FzoxCkyPrwo59YoENT0RvQKL0UHHddxYxlL7dcD-VOdU6WcZrinpIOpuNwU8Js2Lk6IehE"),
    ("news/n22.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vEJSR9VdNaBu1UqgUTlwvhK_H8eAGi3a8uRX9mQzM_H_2m3_wMrUAeUhQOXhUoSM25NNCQpmEZhd4TJXlVXafCY6GJbcnzu7Ak0MW89-Y9yGYGV1gaiVT_kTN61Ftuvx1-IUug3gAavXV0E7mjJUe3Fob9iNfVwQrL5A_zDymKd3jM4qyyf1cJgicemzUNFz72kvel78dtDWFcrGpua1ko_eG56Zx33-S2CYJ7pAQ"),
    ("news/n23.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72utaXYh0w7VmgCCIXqQmYhtxdHXuw7_9mQlNhdkW4o-vFYvX5W6KhVNKsgzhQzjSdofp3OwmGC-czaAZq815JO1nPjgrffGlqqhkosFeNArKP9xlJRxRDWaxlWvUo7RAuVBqjEdOiaHOknd7-fbc6XUFbhY25rmcX3uAcSG3cbDt2DzJ1V875iM7RHDd9JsIVcakJaDL6Bk6qnZmTiTemw1lZtmBFQJGsSFCzOvAgk"),
    ("group/2025-06.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72s8daSp1jrxb_ajAhk67_o0L4afssPzVsJ5eAjuMnxBDqbGKePCxelGlPUzyHjOFN3ZZBHG-VK1Tl82K0e3QjYOkuoyXv9y25YW1UX9IFyLuy_CGrmt-aJulhGTHl8rJKSUIDRq9cP2yTpN-EzKU1xZ-Xhuaq9py4ZyVNsU2tI-tPC62OR3VY05Rq7dO4kVuaMems2BAJux9HElyBR5iEQnz_IwaAZfrNBij-To6fg"),
    ("group/2025-04.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tK7nUxBER8J11wu3UZ9F_1Nk_TlHrdor47nUxH9pWo7m5MEo1GsZmXn_50XFW56i_fhOCRrL9gD5CngIkg4Ay6pveVVKLWTD9GR5degN_8dr_5PIo7ZmGu2dnNe2rptJOvLF23aFB-1W0vSAyPOL8WMaUTj7CpbOc-GT-fM_iq4Hn7G2GnIfiNWBsZrJvHxDAGRzyud2g1pRGnp1mZWWOmKpjDobUa8xow3Wvr"),
    ("group/2023-04.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sKMYr5mq269SZB3V-Uy4MQOStzn2yDd9u-r_XrE4zL1csKIHnaJmLMuX8Tl1bOlEgYbH25dVSj2ta-pLUMKfmJU5N5WBjNUj0W-_EP7qeD2DjDWzHArhQb352ff5XIhWjLV9dw0X1kS6uNeDc9y9IELBvyF-oU0dRPHK3rXUltSWd1h3gxpMQd5YAcoWgceRFPfL8uS8qEUeyiSJKGv72BVmo055b3vVJ5hGhWtI8"),
    ("group/2023-01.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72u0wqHaS-M25ijHlvzEF5rME3iVLlkzKVHpEBtjw2T9y8AgiPPdJGFazlvRVxuxRDei587XgpfY7oGHZLfuwJ5nVEPSUeHwBnvxin2niqGf9DtGMWhVk0awe1LHBR-VnLSOBGAw9xMjVG_A-jb4l9k5ZM_wuivN7ww1GC4yF2d9G7ULWqB4agO71-4Izunj8AG-NPO4ZyfiwwZfHGXZIzxWewh4AI2nyxRko5LO"),
    ("people/choi-sukhoon.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72saDOXrzpQvmaXuOBfLccZZJ5Ybo2xHYpFdWpcmplajtGLpdYYNv3XO1ZdnSpxYa72j4KrYbkMXwAON3gGVYU0_xsKkWxXJRddIuB02MPZgf0NY5IOQRMwisFLHPtfreDTu-ky6OSVPVMQnLiSzPnc2ueO2fCcTkUB1aXow10U7M5jYoCLXgJW9gPZ_tRKwIpQUjiWBhQJ6mTPxjjyzXIqTycqcSv8AzmUp8z_wXyQ"),
    ("people/kim-hyerim.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vXHYlK-kkj2i8hynEdDuLQg86JkUwX2XkDLWkh3lwisAJ15L25akvM-r-pHlPZi7ZqQCVuEJeujeoHUVpW2O09LTkDzWz7uwnhzhr9M41PztCtOw7d5B9ziOV392U08bG28LilreIzoLdLus8EUNCEfZ-wBvDifQ7VhegWZwFbMvmga5IyE_7D4OYmmW4TAbwFyLX7owYzvV0EYA3ED0LM-MroBJ7RoVCQobYCGkM"),
    ("people/huh-eugene.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sUVxE13Uhc6ilDQN9rEEeuympj7MVAeNIKe_F0OvyPfyYEDwf995RfRCUjcuS9fzrw5zG7Jv8tdgQxk5zGZ2yMPyGddAIjJWNrjqa3xsmSIFkK-TYpPYuwcthFPD_4tOZrTC3Uk3IG2beu4szAmKUR_u_JQM_VeI1C2GEh7GPyezfngDYrLd9WYrqKU-KlI4YMLg7VVygiomeMz6zgFuFB28ykBmO6pSefB0RaH2M"),
    ("people/jung-hyein.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72syYNHsvexTGmPoRraraI4sSX_2LC3wG8i4kVaFEGN4_NlepMJj04kbEcL940BYiUSkpIWGrQfeFsgj5N2LeEK3_cmwyjcuMVd3k3fewVCfiZlqAtmOSHCfB7i-8KrBuUf1HB2AiWKqmrsBMWJDrsWPc8STTHvA2YZjGXM7Qa5KIusAAm3bChlAhNwJIVuwWWMpJv3piZIB97SL1bnLnNaV8Ny2EDNEbGy7549PPhE"),
    ("people/ramadhan.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sQi0aqjrl-ct8h-B0FWUHXpNRaObqGIjl4_nFFRS6nttbaTTVQIRG_-C93DFiWoOAe9Cce3Gzm0ylcOn9NngtuXkG14_vgFFNOsDHVajyKyQa92JuaTf88CiE5j960Ypt_NmdqEs2GXx7uIT9abNwG_2yVfYEHfjoi4-hinEriwX0TbNkuAXQx5udYNPj7rcmb2GEbLehtgCnU_cvxo41ldP76VVE_ItJwudsbY_M"),
    ("people/park-yaechan.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72s6zNgT1-6OWD50gBFAilP3LFFFLcTmN6KRhxiAaWpEtvEHNJ39dagTClHCYY3CFS8ok2v4MJRzaMnDVEGe1egSweNKWEEH4nwS2c3ffmXQKiKmLc2j4kOrsZPSlfEHRUTtBbUpwyXl2a_iXJuDQr4rZPeTOKBcQvtD7yif288h3me7QUY02ZpfO2iBZdIuxo90HFx4XLqjqX-5vM2Q771BV2ZVsDbhUHQ9S2VduJI"),
    ("people/park-nayoun.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vGewpMABiQODpyH3hgvWIFUGu-bpGs-X5MzNMzomlhp_PkJ6fl57fuFaXL_J2IXG76e6fHP4CS2EqJpt1ZPikIldn23hiPkvmmgp43vNCod2zv0OI7gxAGvy6zFHomxnfbbU-EIXq-ymqQQ4QPtARv2vOiJqHZydu0iIhx1TiL4tziNg8KIZKMFS_iKtF8z6HjYR3l7Y7m15Cs2Wcvfu1BiVktTk7QMGeLJuSx"),
    ("people/nurul.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uOnDTaNf0KEGajqZPqA5-IKxO8F-TWpU18mrUUg1GLJzzqJmVOQbAvDORGO1EyE43ZWVzxo8acd-f8IcioTEmGtv_gfCJRXJWeBPZFSIVbcI7_ZK6S01Hx_eQAT866EqC2BcD20H7q2iAxhPjjhFAUXs9OtS27Mpg0sssnNaNCVNV1GbLwfdJe-cWh3NMMHy7vuAfK_xtRyMpxVAZ8UFHtkaEw7ILBDCnLbHZT"),
    ("people/kim-jeonghun.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tjo9UcvpcB8tcc6XWmTH4okv5vUIOL5BG5Z10kLuzCsKRHCoTYYILswaZ0pCVQwCgnKQoQhGDgCYgbu_IuV-q6tto-HWIwlKAEDlSQqylspPJyKg-F2-3CA_cVJzPG3uRvB5LMv79mhnKFYV1rCpyi9l079U1dMSe1hQS4M4LZSrHUUWCsAkbg9nSF6UzkW8bj0v7j6_ip0IE6Z58Mj52BqJwfvo-MNFh-X90DYGc"),
    ("people/lee-seoeun.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72upmz_sYz-p8VBjLbZ_B9vLxruAscTPsSKRXiuKn1b2rsDIECPjVJ__RnjMsZsikT5YBdHd_DXlDBzxglSOJ9IiHPQZLV-rIqiMGQ5ptu4atpc8cEAkFs1cUXTTq3cXIA5mXRcCTuQM_1vtf0sn6w3btbiyGjdhSvD70RYT7Q2XsGFyfNePsPjYOpLlya8E52bK8diCC1NR0scsXv13ny0WHnVH6oElecXwxVoOUeM"),
    ("people/lee-taeung.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sWWX0x5sxAu49fHSjCtv6CPrQoqIRQCTbh9NctElZdvNJ6wdNZ8R_FZ88GMe877VBa59VdRwTMoFT5DL2AX_saP2yu17nhlVPR1oNiBWUHOkWoh4uFpKg8EqPYS-yYAC64Y1E_dXHNawKJG0OX-quVVgd1yX3GiAgbyYXyenbIovEvqpXpwWbsg8LQR5ZkoRtLg1DMfcjjh54jMEMg0KBmgqLInHSN5EBr6GuS"),
    ("people/park-sohui.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uZdDa4_NjaAB9nx9QgEqAfBV8NC2iTk2vjYUUAWvbfLY5nU8-usuTTPEFest6KF_oLzYIXtw7ArMsF6uxaKoivWpjPAD575oNknPH0lBWqdPz4PpNETqLcNw9Pm-8f57AvED2k1eBgnPVzDsuR9FYPvIvtL4jOHfq2xkX1BU3aEP6yeOgSP6wNHb73HAdkRmmf4Lseeu1GK1F6vUG0EoqYvOz0TgLWgDvWz7HW"),
    ("people/kim-kyeongsu.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tv63-qXX3tBjtOYoCVnISeN6DXe0pxFov4whlVSKmoembJ75-1CkbIz-pVuNzlE_GWWNL3ZwleLZ6fkc7B-poobzjNuT2XXM7UU-FzCfWNz1QmeTcXHkVAS1sWQziJ0zHTv9nc8Q7lRkv5Pop32EcSHzB9jssbOp-rm2I9hIULJpvFAL00X0PKtf-KPJs_WQbegQAR7orWQqqHZakOdePV9UD3Q3q1jzwFdJgH"),
    ("research/biomass-jetfuel.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72t2Jt6RCDlDu3eqG8ZnP12sqHGx2JcCCUZnc_KriNIEyAlL6lYLOJjTF096r0EYu9XV-A5AmWWtP0rliKXRh_IDYwR4fwxj9RQvxGaVvKdxNPtUk1sLmi8UGbtUxmSsrlCl6t1LNmHzABHGe4eA5QtektxzANM-2ykYDqZf4rYDUwAacp0vjl19NHWgGy4H1tOf6JAe4pLoKZj5KnjhfSwyIIAMOPtPWFcSQSAq3TI"),
    ("research/co2-rcc.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uOvigk1hqs8fMF7j6npDcGCxM0atmAKkBvVV813Dis62P7kqoTpb3IM9bRlghLHTdLhjHQ6g5xgDDhvfg8sZPV8mPcEGNEAhchI8XOXe2Px90mX6yODVk6fCnBXQYGO_JX0LX8QPn2f77uZVLj-bbnfis_NJlhQ48Nj4LHJovXfflJ_UCE5GmJdj2bfPh75Nb5POI8jE3dzA52JJ7zJCUSH1mrZwp8qCnet9ljxio"),
    ("research/co2-dac.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72tp3v1M5fZnKYKZFazOsdl0w10W9kDMZ6R7i37Vt1dw5hZJNArG57w4C_6vyTMDH0JYO-t8kVGpapY_HGG99bNQ2ZIxSMYykq9nUD8XWATEBR6bytHX3GUAzY4x_0G8Um41q-RuO6Gb_ftGt9oRBpqV4CpeZGJVwJCMq1krW7T3m93-21OesBesOAuYzXvD8_gtVa5EoBQyxShiq5_1OatowbdQRK7CKwVUEVU3wL0"),
    ("research/dft-1.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sgjt6V5jforbXMyfTsYK0EXgqeNv76cUTEr9cKc7G61cFFSs4VYkt9pzOyk7e47PcU-bOtL3bTgNx0W6SaQLkgFhoAXD4QE9ZWupw6eyB781joDw6oHt6459_Q7uvVbl43lC8gkEBuIOaJ5muGDOPa6YUIowudF5IwdYsqA0QfUkCfE03eSGQJeyjer8JuTYWd1xvhOQxqdhP1sixoSbuXaR6DragI0cpSme8dTZ4"),
    ("research/dft-2.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72upP49OifpbEZpdJKJ-tLre998SA5JWpSQqUM0T8bCMqXGF-YLeYQcYYUzt8SLzzXYLtG2pU7bfqkYSROqHwzz_QMPwstW58H2ihxDwa5Ko_olr83VFfAbseua5sRbxXSq3QX_LUhulGEkT8TuvnJParo16_nFa4rmXqKcXUH_EJ0G_5gqu82ZSU005fx1GyaQ05QRV2Mkc2fPsTfkKdght0MEbA1Ede4j7OSmq"),
    ("research/dft-first-principles.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72ulQnjM10BTLPjrZV-cudp5-1Q9RtT3jHmR0B2BkIdIU3n2nCjl_7o-y3HVvhA8eCpuzaXxr7hfotTcrLWFOdzl-hkXFdUhXCJOQzQ_QzIOCAuBYoOqwkaZIbqZJFcGiSMHeCVjBhcymt0VcnM0M6mZlZMLDPbatmbrysPlD0bAuYDDB_1K4g1i07JqhaBdx2m72NTVdZg_glwFtnWOTVlHlNvbi6lEROo_eKN4OPY"),
    ("research/dft-electronic.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72trSBFZ4wFCZMhRFwv4OSM-GD0Ti5gyJlfEW9QjsV1_NFXoViyNqGr5EnJLbQX_ahwhEgCMgrvZyWIr1PnePzUZdlrZQ_4F0BwXU63f-KquS23hKTazERrGK5pOinmTpKpiDSriU932V5m6VE7y7nYFUB3t5uE4kWUxbjL5yytbv8g6H_kaF57EDMXt136yird6_u0l42cpj81clB-84CvndshVX8gHLTU_IKCzfKM"),
    ("research/dft-mechanism.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uzpiuRAkJl8uDFvQrJoM6tngL2GdqMQqgfi7Lnp0FPGgVIJ7PcXXFrapfOS358Q0cG48T_lUb8NCQ6_y4ejBsEuNdk5OKQu5LoM9iKeKpcf60jleoqQDvv0jVYyLSAC0cXAxowA0QNJuBNUxL_dADkE12Mw7jSuZ0b5Dcpve6d_vUw3ue5iswE7PLj9suCW0h_oCf8RBWC_n6C0cKUEwQS4u4t7ZmTkWzRzuzt"),
    ("research/ml-screening.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uT3EMWsEaArNvI8J_hxb6OPIyB2Hu-QfrXoe48egnfk4Rp-QIEeCuLwB-cBMymDqi6-ytixukhkjzWaPCLnWGLbUycljPL0iSOpvCIab7DwP2yL_3tc6sgP0It8YfXC99UkQZpN2FpxorRccCup_JPLXgjonvG21jwuICk5Qaut0YXW9ZKCuBobnTDUsIYlYQbji9fjcyQmsumvqMnDsGLLfyg-A-AYzfGKaXAlio"),
    ("research/ml-digital.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72stFMXpVECYPT0FNhUv2yOrtha4ryXrznnlsOuJuJ72U3L675jvYz6JYBtsUZmWhiEVgN6J85kGb97yyLxHX4ZF6dGQN1daezwWgvMuFFOM4LI4B2BbROsWVu7rhf0SGnaz5esiRZa99VnaqnLkTAeq1uOx64HqrS9aZWcYr2kwGWEeKhsI2uLaXrQ1toyfrdshauLOQq5iMDOFYnBtvM2aRhnyuBXQQKzk7zqjvnw"),
    ("research/ml-multimodal.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uRgBMwu9nGulit3-DGFMUu-B6pajEIUahWOED8eEz1Jgs6RbEuoKBCWi7xhioutQzQ6h1ZESnHcqN7sKt1h4pdxeVeQKeltLPSXUEk9DU8L3dURUDjhg_ykmoEkBSJJs7YbCPrMli3x3LW-FK8HZIJB1GvSNDHtY6aQg8DDNBAHz3NgDAc0GuC9LDVIJs2NnOTBoEN9xxXj2LG6RVxJoGV9rj8v4b16RQUSeBz4Fk"),
    ("research/ml-incremental.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72vgnV2Xe2VFA3_zDfuUgvV7YcgKV6q3HviqT5Pz96Uj4Ws8AsYkYD4H_Xjj2w-ihG0gCmVJD9Rb1O20PxfhJ7KaBMXWHu8TbJOa2OUooRh3XBJG2P0z8lq7xZihmEmSt6rX59qKsIDS-Y5Pflb_dJjiAHR_ihQ4m94XcifpVAIUCaq8jzM8MJxRXNR2o4sv6K0izTH4VjSQPqk-_Q-dSJH1q6noo9OLoDUBdvZaVg4"),
    ("research/ml-xai.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uEkwHaZKOE7tIvlGz2cQnJavUlLfFDdlZDOzlimz1HK1UQe-xbyHLJLDWsS4wEQTvHV9JVAjPe253C3A4TWf3UYOvmG7T6BRPM2h0D1SU6WpgUpKDrH5_InN4EV-AxJBhVvjzv7_jQFf1OullgnFIkSDR5-awMCMKTkYH14E6H4bUheh0QHBz_lsXNnI1wqt_UOFgKsxoKYB_VrOLqUOTsYzjCa2Llu7DPFqQ9GKk"),
    ("research/ps-modeling.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sAF1Kqbk8h89_ntar7iuI9uNkL8oX-HLUFtEOnRVkhHT2Pjle4zn3AVp06_AbA7kowLTlGfQW7_YxrY29GA-1XsQbFNmrYLQCQ7EMWyNkbajCDgyPIU44vbPAesXYi4Wo9MkwWa23WAwnI9_HdCOMxESF91bM10K9nsJuzV9kvbxKnkKC7eCaQcOzqQi-7so3x26tOZkQJ9Qk_XFUBuOT8y4fN68b2ayvLTxnATJI"),
    ("research/ps-tea-lca.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72veSdwKoyphBjikqJzWr4yQhLsjuI4nzKwXf803WDqISC2-PbBVjV5vwdLJ4LBRze7ggj6Q74_P2uivt0venkSW5F8jdBx34tfoec-gFdmJSjpjFeo_uwXPD6uT2SXpxOGqc8id4OOhmGEZcxIkqyzK3JNvKCdVt3QTGjAYVV3mb6AJFBR8yAGEh1rmX3pKkhunvAzKgRV_9VRtCX-AVohIzvpAsHdJdonylwRYmS8"),
    ("research/pu-overview.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sK4IQwV8wK-ipFUKlwz3Zk4h5l-NN9F0O55Vf6XBkHcEWCl1o6cLxhxcNjim424jzzvcLillqM-nFVEhgfsZhIWf8DRnH-qNehnjOi6R_59ilI6WulFTTI66BF_oZsiPUdG5WUqNu5G0XLnXrv81QxwesrPcXYgs1x-6-ZjzXBRVFqWpR_43AF5y27ojvrDdzsAS6tGVhQfvlKMQ6vHqqGYlypWtL39gb5fllLdzg"),
    ("research/pu-kmc.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sRZdVTog09CsjmJmfetOe9QXU9EFYz0Ip0h18262sIIT2p63V01igW38hY3ZHovSWa60oHSSxuFPda04Vip6y5ppwe-S2dqDamh-Iuij6ivzox8dX5_7WRFmjt9uuGVAggbufYChH9PIt75nMFGK2LIKiZrLhX0jIX93t5AfxeXWfGSciwLHgHxQ7210NtY7zKI1TA6YmRJPLc8244V7lUOZZ9wPsOPeTATmct"),
    ("research/pu-plasma.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72sUJQxAqFH-4SY5DJTbHkrct7108pbEd-2HDKYstQ5uhiYKHGnk6lSxWnozqh7O0NN59LXQP9ffrjJwdabSZ43x_1lRk8euZLcRlug_NODv-MT8MpBYXzwJMAPrRdhLms3pGBoH0cvlOLYkAofXuvqoAoVKcZ2rEhHMiPkZZ4gnEuAmk93x-xFeDp8L5C_MuR3RE3AGuSWq78BbH3KqR2C3IY_5zb6G0L_WsmltFXk"),
    ("research/cluster.jpg", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72un8CVIm9Z6sGs6uxNb-cDJ5KLYFtq9h9SJNZSaIAFtUbbwrkDYAawzdXayb6OgF0pPYVO5d6CJqJJosOSk4b1tepSgd_iUKoPpW7mo1w_N2KUuqkJctHptrds8irl7KgS3Wg5N9kdhdALhNp2VuN56uTSGK4jlfi8ciJDjDDl4eA2e8K_3yT3FbLWVEx9CsfZ7wdUGstMWfoMzWxPlt3xVCoZMlPFaSe5IHOiYoxs"),
    ("misc/logo.png", "https://lh7-us.googleusercontent.com/sitesv-images-rt/AMxu72uAY_W7W0GyfiYRzhbkq7XP7zpnD8OEQAM6yCk7XkehiMt_F6p-KgDzl6Ldzg6LSmaTjvTAIDBrXjJ8jT2rvWQC-T7od28Y0kH2CgSK-Nf9ztIg9Joj10Ro2YPt3drlWSbdbVuPaw4bImq7Sgog3pf7QbxieS0Y4nT0lWopNQYX3ZlYoHfFzvTWmIxdeTA"),
]


def main():
    force = "--force" in sys.argv
    ok = skipped = failed = 0
    for rel, url in IMAGES:
        dest = os.path.join(ROOT, rel)
        if os.path.exists(dest) and not force:
            skipped += 1
            continue
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            req = urllib.request.Request(f"{url}=w{WIDTH}", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                data = r.read()
                ctype = r.headers.get("Content-Type", "")
            if not ctype.startswith("image/"):
                raise RuntimeError(f"not an image ({ctype}); the network may be blocking Google")
            with open(dest, "wb") as f:
                f.write(data)
            ok += 1
            print(f"  ok    {rel}  ({len(data) // 1024} KB)")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"  FAIL  {rel}: {e}")
    print(f"\n{ok} downloaded, {skipped} already present, {failed} failed")


if __name__ == "__main__":
    main()
