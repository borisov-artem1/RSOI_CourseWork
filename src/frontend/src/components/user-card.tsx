import React from 'react'
import Text from './text';
import { UserInterface } from '../model/interface/user.interface';
import AuthService from '../services/auth-service';

interface UserCardProps {
  useName?: boolean;
  user: UserInterface | undefined;
  className?: string;
}

export default function UserCard({
  user,
  className,
  useName = true,
}: UserCardProps) {
  return (
    <div className={className}>
      {useName &&
        <React.Fragment>
          <Text size="medium" className="font-extrabold">{user?.login}</Text>
          <br />
        </React.Fragment>
      }

      <div className="flex flex-row gap-2">
        <Text className="font-semibold min-w-32" size="medium">Фамилия:</Text>
        <Text size="medium">{user?.lastname ?? "???"}</Text>
      </div>
      <div className="flex flex-row gap-2">
        <Text className="font-semibold min-w-32" size="medium">Имя:</Text>
        <Text size="medium">{user?.firstname ?? "???"}</Text>
      </div>

      <br />
      <div className="flex flex-row gap-2">
        <Text className="font-semibold min-w-32" size="medium">Почта:</Text>
        <Text size="medium">{user?.email ?? "???"}</Text>
      </div>
      <div className="flex flex-row gap-2">
        <Text className="font-semibold min-w-32" size="medium">Телефон:</Text>
        <Text size="medium">{user?.phone ?? "???"}</Text>
      </div>

      {AuthService.isAdmin() && 
        <div className="flex flex-row gap-2">
          <br />
          <Text className="font-semibold min-w-32" size="medium">Роль:</Text>
          <Text size="medium">{user?.role ?? "???"}</Text>
        </div>
      }
    </div>
  )
}
