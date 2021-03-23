
void * FUN_0040078d(int param_1)

{
  int iVar1;
  time_t tVar2;
  void *pvVar3;
  int local_c;
  
  tVar2 = time((time_t *)0x0);
  DAT_00601074 = DAT_00601074 + 1;
  srand(DAT_00601074 + (int)tVar2 * param_1);
  pvVar3 = malloc((long)(param_1 + 1));
  if (pvVar3 != (void *)0x0) {
    local_c = 0;
    while (local_c < param_1) {
      iVar1 = rand();
      *(char *)((long)local_c + (long)pvVar3) = (char)(iVar1 % 0x5e) + '!';
      local_c = local_c + 1;
    }
    *(undefined *)((long)pvVar3 + (long)param_1) = 0;
    return pvVar3;
  }
                    /* WARNING: Subroutine does not return */
  exit(1);
}

